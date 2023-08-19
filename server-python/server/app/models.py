from django.db import models

# Create your models here.

class Endpoint(models.Model):
    '''
    Attributes:
        name: tên của endpoint dùng trong API URL,
        owner: tên người sở hữu,
        created_at: ngày khởi tạo endpoint.
    '''
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class MLModel(models.Model):
    '''
    Attributes:
        name: tên mô hình.
        description: giới thiệu về mô hình.
        version: quản lý phiên bản.
        owner: chủ sở hữu.
        created_at: ngày khởi tạo mô hình.
        parent_endpoint: khóa ngoại của bảng Endpoint.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

class MLModelStatus(models.Model):
    '''
    The MLAlgorithmStatus represent status of the MLAlgorithm which can change during the time.

    Attributes:
        status: Trạng thái của mô hình: testing, staging, production, ab_testing.
        active: tồn tại hay không tồn tại format boolean.
        created_by: tên người tạo.
        created_at: ngày khởi tạo trạng thái.
        parent_mlmodel: khóa ngoại của bảng MLModel.

    '''
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlmodel = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name = "status")

class MLRequest(models.Model):
    '''
    Lưu lại toàn bộ request liên quan đến mô hình
    Attributes:
        input_data: input của mô hình dưới dạng Json.
        full_response: kết quả raw của mô hình (optional).
        response: kết quả của mô hình dưới dạng Json.
        feedback: feedback của người dùng (optional).
        created_at: ngày khởi tạo request.
        parent_mlalgorithm: khóa ngoại của bảng MLModel.
    '''
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlmodel = models.ForeignKey(MLModel, on_delete=models.CASCADE)
