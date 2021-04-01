import 'dart:io';

import 'package:yieldup/app/shared/models/service_response.dart';

abstract class ITensorflowService {
  Future<ServiceResponse> loadModel();
  Future<ServiceResponse> classifyImage(File image);
}
