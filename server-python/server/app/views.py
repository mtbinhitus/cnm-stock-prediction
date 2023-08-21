from django.shortcuts import render
from django.db import transaction

import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from server.wsgi import registry

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
        algorithm_name = sticker + '_' + model + '_' + '_'.join(indicator)
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

        # Load historical data from binance api\
        api_key = 'BINANCE_API_KEY'
        api_secret = 'BINANCE_API_SECRET_KEY'
        api_endpoint = 'BINANCE_API_ENDPOINT'

        instance = BinanceAPIManager(api_key, api_secret, api_endpoint)

        data_btc = instance.get_historical_klines(symbol='BTCUSDT', interval='1h', startTime=dt.datetime.now() - dt.timedelta(days=3), endTime=dt.datetime.now())
        df_btc = instance.get_dataframe_from_bars(bars=data_btc)
        utils.df_to_csv(df=df_btc, filename="btc_bars")
        data_predict = df_btc

        prediction = algorithm_object.compute_prediction(data_predict)

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