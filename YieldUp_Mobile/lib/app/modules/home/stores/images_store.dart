import 'dart:io';

import 'package:flutter_modular/flutter_modular.dart';
import 'package:mobx/mobx.dart';
import 'package:yieldup/app/modules/home/services/image_picker_service_interface.dart';
import 'package:yieldup/app/modules/home/services/tensor_flow_service_interface.dart';
import 'package:yieldup/app/shared/global_variables.dart';
import 'package:yieldup/app/shared/models/diagnosis_result.dart';
import 'package:yieldup/app/shared/models/service_response.dart';
import 'package:yieldup/app/shared/navigation.dart';
part 'images_store.g.dart';

class ImagesStore = _ImagesStore with _$ImagesStore;

// flutter packages pub run build_runner build

abstract class _ImagesStore with Store {
  final IImagePickerService _imagePickerService;
  final ITensorflowService _tensorflowService;
  _ImagesStore(this._imagePickerService, this._tensorflowService);

  @observable
  String error;

  @observable
  DiagnosisResult result;

  @observable
  File selectedImage;

  @action
  void setError(String error) {
    this.error = error;
  }

  @action
  void setResult(DiagnosisResult result) {
    this.result = result;
  }

  @action
  void setSelectedImage(File image) {
    this.selectedImage = image;
  }

  Future<void> loadModel() async {
    ServiceResponse serviceResponse = await _tensorflowService.loadModel();
    if (!serviceResponse.success) {
      setError(serviceResponse.message);
    }
  }

  Future<void> getImage(ImageFrom imageFrom) async {
    ServiceResponse serviceResponse =
        await _imagePickerService.getImage(imageFrom);
    if (serviceResponse.success) {
      File image = serviceResponse.data as File;
      setSelectedImage(image);
      await processImage(image);
    } else {
      setError(serviceResponse.message);
    }
  }

  Future processImage(File image) async {
    ServiceResponse serviceResponse =
        await _tensorflowService.classifyImage(image);
    if (serviceResponse.success) {
      List<DiagnosisResult> diagnosisResults = List.from(serviceResponse.data);
      setResult(diagnosisResults.first);
      navigateToPageAndRemoveAllPreviousPages('/', arguments: 1);
    } else {
      setError(serviceResponse.message);
    }
  }
}
