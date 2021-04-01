import 'package:flutter/material.dart';

class DiagnosisResult {
  double confidence;
  int index;
  String label;

  DiagnosisResult({
    @required this.confidence,
    @required this.index,
    @required this.label,
  });

  factory DiagnosisResult.fromJson(Map<String, dynamic> json) {
    return DiagnosisResult(
      confidence: json["confidence"],
      index: json["index"],
      label: json["label"],
    );
  }
}
