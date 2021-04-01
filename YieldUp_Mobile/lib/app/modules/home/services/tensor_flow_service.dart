import 'dart:io';

import 'package:flutter/services.dart';
import 'package:tflite/tflite.dart';
import 'package:yieldup/app/modules/home/services/tensor_flow_service_interface.dart';
import 'package:yieldup/app/shared/models/diagnosis_result.dart';
import 'package:yieldup/app/shared/models/service_response.dart';

class TensorflowService extends ITensorflowService {
  @override
  Future<ServiceResponse> classifyImage(File image) async {
    try {
      var recognitions = await Tflite.runModelOnImage(
          path: image.path, // required
          imageMean: 0.0, // defaults to 117.0
          imageStd: 255.0, // defaults to 1.0
          numResults: 2, // defaults to 5
          threshold: 0.2, // defaults to 0.1
          asynch: true // defaults to true
          );
      var diagnosisResults = recognitions
          .map((recognition) {
            return DiagnosisResult.fromJson(Map.castFrom(recognition));
          })
          .toList();
      diagnosisResults.sort((a, b) => b.confidence.compareTo(a.confidence));
      return ServiceResponse(success: true, data: diagnosisResults);
    } catch (e) {
      if (e is PlatformException) {
        return ServiceResponse(success: false, message: e.message);
      }
      return ServiceResponse(success: false, message: e.toString());
    }
  }

  @override
  Future<ServiceResponse> loadModel() async {
    try {
      await Tflite.loadModel(
        model: "assets/model_unquant.tflite",
        labels: "assets/labels.txt",
        numThreads: 1,
        isAsset: true,
        useGpuDelegate: false,
      );
      return ServiceResponse(success: true);
    } catch (e) {
      if (e is PlatformException) {
        return ServiceResponse(success: false, message: e.message);
      }
      return ServiceResponse(success: false, message: e.toString());
    }
  }
}
