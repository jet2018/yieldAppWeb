import 'package:flutter/material.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:yieldup/app/modules/home/results/results_controller.dart';
import 'package:yieldup/app/shared/utils.dart';

class ResultsComponent extends StatefulWidget {
  @override
  _ResultsComponentState createState() => _ResultsComponentState();
}

class _ResultsComponentState
    extends ModularState<ResultsComponent, ResultsController> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Results"),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            flex: 2,
            child: controller.imagesStore.selectedImage != null
                ? Image.file(
                    controller.imagesStore.selectedImage,
                    fit: BoxFit.cover,
                  )
                : Container(),
          ),
          Expanded(
            flex: 3,
            child: controller.imagesStore.result == null
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        "No results yet.\n Diagnoze to receive a result.",
                        textAlign: TextAlign.center,
                        style: TextStyle(
                            fontWeight: FontWeight.w800, fontSize: 18.0),
                      ),
                    ),
                  )
                : Container(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        ListTile(
                          dense: true,
                          visualDensity:
                              VisualDensity(horizontal: 0.0, vertical: 0.0),
                          title: Text(
                            "Detected Disease",
                            style: TextStyle(fontWeight: FontWeight.w800),
                          ),
                          trailing: Text(
                            controller.imagesStore.result.label.split(" ").last,
                          ),
                        ),
                        ListTile(
                          dense: true,
                          visualDensity:
                              VisualDensity(horizontal: 0.0, vertical: 0.0),
                          title: Text(
                            "Accuracy",
                            style: TextStyle(fontWeight: FontWeight.w800),
                          ),
                          trailing: Text(
                            "${(controller.imagesStore.result.confidence * 100).toStringAsFixed(3)} %",
                          ),
                        ),
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 20.0),
                          width: double.infinity,
                          child: Card(
                            elevation: 0.0,
                            child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Center(
                                child: Text(
                                  "${getCodeGivenDiseaseLabel(controller.imagesStore.result.label.split(" ").first)}",
                                  style: TextStyle(
                                    fontSize: 20.0,
                                    fontWeight: FontWeight.w700
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                        SizedBox(height: 10.0),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16.0),
                          child: Text(
                            "Please enter the above code in the diagnosis part of web application for remedy",
                            textAlign: TextAlign.center,
                          ),
                        ),
                        TextButton(
                          onPressed: () async {
                            final url = "https://yieldupp.herokuapp.com";
                            if (await canLaunch(url)) {
                              await launch(url);
                            }
                          },
                          child: Text("Visit web application"),
                        ),
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
