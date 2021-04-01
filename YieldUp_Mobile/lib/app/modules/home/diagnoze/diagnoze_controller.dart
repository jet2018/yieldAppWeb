import 'dart:io';
import 'package:mobx/mobx.dart';
import 'package:yieldup/app/modules/home/stores/images_store.dart';
import 'package:yieldup/app/shared/global_variables.dart';

part 'diagnoze_controller.g.dart';

class DiagnozeController = _DiagnozeController with _$DiagnozeController;

// flutter packages pub run build_runner build

abstract class _DiagnozeController with Store {
  final ImagesStore _imagesStore;
  _DiagnozeController(this._imagesStore);

  @observable
  bool busy = false;

  @action
  void setBusy(bool value) {
    busy = value;
  }

  Future<void> getImage(ImageFrom imageFrom) async {
    setBusy(true);
    await _imagesStore.getImage(imageFrom);
    setBusy(false);
  }
}
