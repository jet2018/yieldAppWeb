import 'package:yieldup/app/shared/global_variables.dart';
import 'package:yieldup/app/shared/models/service_response.dart';

abstract class IImagePickerService {
  Future<ServiceResponse> getImage(ImageFrom imageFrom);
}
