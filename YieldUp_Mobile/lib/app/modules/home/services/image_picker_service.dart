import 'dart:io';

import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:yieldup/app/modules/home/services/image_picker_service_interface.dart';
import 'package:yieldup/app/shared/global_variables.dart';
import 'package:yieldup/app/shared/models/service_response.dart';

class ImagePickerService implements IImagePickerService {
  final imagePicker = ImagePicker();
  Future<ServiceResponse> getImage(ImageFrom imageFrom) async {
    try {
      PickedFile pickedFile;
      if (ImageFrom.Camera == imageFrom) {
        pickedFile = await imagePicker.getImage(source: ImageSource.camera);
      } else if (ImageFrom.Gallery == imageFrom) {
        pickedFile = await imagePicker.getImage(source: ImageSource.gallery);
      }
      
      if (pickedFile != null) {
        File file = File(pickedFile.path);
        return ServiceResponse(success: true, data: file);
      } else {
        return ServiceResponse(success: false, message: "No image selected");
      }
    } catch (e) {
      if (e is PlatformException) {
        return ServiceResponse(success: false, message: e.message);
      }
      return ServiceResponse(success: false, message: e.toString());
    }
  }

}
