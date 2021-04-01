import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:yieldup/app/app_widget.dart';
import 'package:yieldup/app/modules/home/home_module.dart';

class AppModule extends MainModule {
  @override
  List<Bind> get binds => [];

  @override
  Widget get bootstrap => AppWidget();

  @override
  List<ModularRouter> get routers => [
    ModularRouter(
      "/",
      module: HomeModule(),
      transition: TransitionType.fadeIn,
    ),
  ];

}