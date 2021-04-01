import 'dart:io';
import 'package:mobx/mobx.dart';
import 'package:yieldup/app/modules/home/stores/images_store.dart';
import 'package:yieldup/app/shared/global_variables.dart';

part 'home_controller.g.dart';

class HomeController = _HomeController with _$HomeController;

// flutter packages pub run build_runner build

abstract class _HomeController with Store {
  final ImagesStore imagesStore;
  _HomeController(this.imagesStore);

  @observable
  bool busy = false;

  @action
  void setBusy(bool value) {
    busy = value;
  }

   Future<void> getImage(ImageFrom imageFrom) async {
    setBusy(true);
    await imagesStore.getImage(imageFrom);
    setBusy(false);
  }
}
