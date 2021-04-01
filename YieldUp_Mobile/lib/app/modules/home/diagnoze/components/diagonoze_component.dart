import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:yieldup/app/modules/home/home_controller.dart';
import 'package:yieldup/app/shared/components/custom_button.dart';
import 'package:yieldup/app/shared/global_variables.dart';

class DiagonozeComponent extends StatefulWidget {
  @override
  _DiagonozeComponentState createState() => _DiagonozeComponentState();
}

class _DiagonozeComponentState
    extends ModularState<DiagonozeComponent, HomeController> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Diagnoze"),
      ),
      body: Observer(
        builder: (context) {
          if (controller.imagesStore.error != null) {
            print(
                "????????????!!!!!! ${controller.imagesStore.error}");
          }
          return Center(
            child: CustomButton(
              isActive: true,
              isBusy: controller.busy,
              title: "Add image to diagnoze",
              onPressed: () => showModalBottomSheet(
                context: context,
                builder: (BuildContext context) => Container(
                  padding: const EdgeInsets.symmetric(
                      vertical: 20.0, horizontal: 8.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      CustomButtonWithoutColor(
                        borderColor: Theme.of(context).primaryColor,
                        title: "Camera",
                        onPressed: () async {
                          Navigator.pop(context);
                          await controller.getImage(ImageFrom.Camera);
                        },
                      ),
                      SizedBox(height: 10.0),
                      CustomButtonWithoutColor(
                        borderColor: Theme.of(context).primaryColor,
                        title: "Gallery",
                        onPressed: () async {
                          Navigator.pop(context);
                          await controller.getImage(ImageFrom.Gallery);
                        },
                      ),
                      SizedBox(height: 10.0),
                    ],
                  ),
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(cardBorderRadius),
                    topRight: Radius.circular(cardBorderRadius),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
