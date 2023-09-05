from django.shortcuts import render
from django.db import transaction

import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from server.asgi import registry

from rest_framework import viewsets
from rest_framework import mixins

from app.models import Endpoint
from app.serializers import EndpointSerializer

from app.models import MLModel
from app.serializers import MLModelSerializer

from app.models import MLModelStatus
from app.serializers import MLModelStatusSerializer

from app.models import MLRequest
from app.serializers import MLRequestSerializer

from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
from ml.api.binance_websocket import BinanceAPIManager
import ml.api.utils as utils
import datetime as dt
import pandas as pd

# Create your views here.

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLModelSerializer
    queryset = MLModel.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = MLModelStatus.objects.filter(parent_mlmodel=instance.parent_mlmodel,
                                                created_at__lt=instance.created_at,
                                                active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLModelStatus.objects.bulk_update(old_statuses, ["active"])


class MLModelStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = MLModelStatusSerializer
    queryset = MLModelStatus.objects.all()

    # gọi bởi CreateModelMixin class để lưu một object mới
    def perform_create(self, serializer):
        try:
            # quản lý các tiến trình nhỏ trong Django transaction. Success thì active == True và ngược lại
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))


class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()


# XGBoost: xgboost, RNN: rnn, LSTM: lstm, TransTE: transte

# Close: close, Price of Change: poc
# Relative Strength Index: rsi
# Bolling Bands: bb
# Moving Average: ma
# Standard Deviation: sd

class PredictView(views.APIView):
    def get(self, request, endpoint_name):
        return Response('Class based view')
    def post(self, request, endpoint_name, format=None):

        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")
        sticker = request.data.get('sticker')
        model = request.data.get('model')
        indicator = request.data.get('indicator')
        # tính name của model
        if sticker is None:
            return Response(
                {"status": "Error", "message": "Missing sticker information."},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        if model is None:
            return Response(
                {"status": "Error", "message": "Missing model information."},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        if indicator is None:
            return Response(
                {"status": "Error", "message": "Missing indicator information."},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        sticker = request.data['sticker']
        model = request.data['model']
        indicator = request.data['indicator']
        indicator.sort()

        algorithm_name = sticker + '_' + model
        algorithm_name = algorithm_name.lower()
        # return Response(algorithm_name)

        algs = MLModel.objects.filter(parent_endpoint__name = endpoint_name, name = algorithm_name, status__status = algorithm_status, status__active=True)
        
        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]

        df_btc = pd.read_csv("./btc_bars.csv")
        df_btc['date'] = [dt.datetime.fromtimestamp(x / 1000.0) for x in df_btc.time]
        df_btc.set_index('date', inplace=True)
        data_predict = df_btc[len(df_btc)-200:]
        print(data_predict)

        prediction = algorithm_object.compute_prediction(data_predict, indicator=indicator)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlmodel=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)
    

class BinanceAPI(views.APIView):
    def get(self, request, format=None):
        # Load historical data from binance api

        # req_symbol = self.request.query_params.get("symbol")
        req_limit = int(self.request.query_params.get("limit"))
        try:
            df_btc = pd.read_csv("./btc_bars.csv")
            df_btc.drop(df_btc.columns[[0]], axis=1, inplace=True)
            print(df_btc.tail(5))
            if req_limit <= len(df_btc):
                output_data = df_btc[len(df_btc) - req_limit:].to_dict(orient='records')
                print(len(output_data))
                return Response(output_data, status=status.HTTP_200_OK)
            elif req_limit > len(df_btc):
                output_data = df_btc.to_dict(orient='records')
                print(len(output_data))
                return Response(output_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"status": "Error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            ) 

import plotly.express as px
from django.shortcuts import render
from ml.btc_sticker.btc_xgboost import BTCPredictionUsingXGBOOST
from ml.btc_sticker.btc_rnn import BTCPredictionUsingRNN
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
def plotly(request):
    indicator = ["close"]
    model = 'xgboost'
    algo = BTCPredictionUsingXGBOOST()
    if request.method == 'POST':
        model = request.POST.getlist('model')
        model = model[0]
        indicator = request.POST.getlist('indicator')
        if(len(indicator) == 0):
            indicator = ["close"]
        print("Indicator request",indicator)
        print("Model request",model)
    models = [{"name": "XGBoost", "value": "xgboost", "check": True}, {"name": "RNN", "value": "rnn", "check": False}, {"name": "LSTM", "value": "lstm", "check": False}]
    indis = [
        {"name": "Close Price", "value": "close", "check": True},
        {"name": "Rate Price of Change", "value": "roc", "check": False},
        {"name": "Bollinger Bands", "value": "bb", "check": False},
        {"name": "Moving Avarage", "value": "ma", "check": False},
        {"name": "Standard Deviation", "value": "sd", "check:": False},
        {"name": "Relative Strength Index", "value": "rsi", "check:": False},
        {"name": "MACD", "value": "macd", "check:": False},
    ]

    for indi in indis:
        if indi['value'] in indicator:
            indi['check'] = True
        else:
            indi['check'] = False

    if(model == "xgboost"):
        algo = BTCPredictionUsingXGBOOST()
        models[0]["check"] = True
        models[1]["check"] = False
        models[2]["check"] = False
    elif (model == "rnn"):
        algo = BTCPredictionUsingRNN()
        models[0]["check"] = False
        models[1]["check"] = True
        models[2]["check"] = False
    elif (model == "lstm"):
        algo = BTCPredictionUsingLSTM()
        models[0]["check"] = False
        models[1]["check"] = False
        models[2]["check"] = True
    print(type(algo))
    fig_line = algo.visualize(indicator)
    # fig_line = px.line(data_predict, x="lifeExp", y="gdpPercap", color="country", text="year", height=300)
    # fig_line.update_traces(textposition="bottom right")

    line_chart = fig_line.to_html(full_html=False, include_plotlyjs=False)

    return render(request, "plotly.html", {
                                           "line_chart" : line_chart,
                                            "indis": indis,
                                           "models": models,})