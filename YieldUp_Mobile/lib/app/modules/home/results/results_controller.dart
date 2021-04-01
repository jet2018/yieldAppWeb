import 'package:mobx/mobx.dart';
import 'package:yieldup/app/modules/home/stores/images_store.dart';

part 'results_controller.g.dart';

class ResultsController = _ResultsController with _$ResultsController;

// flutter packages pub run build_runner build

abstract class _ResultsController with Store {
  final ImagesStore imagesStore;

  _ResultsController(this.imagesStore);
}
