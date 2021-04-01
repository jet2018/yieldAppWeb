// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'diagnoze_controller.dart';

// **************************************************************************
// StoreGenerator
// **************************************************************************

// ignore_for_file: non_constant_identifier_names, unnecessary_brace_in_string_interps, unnecessary_lambdas, prefer_expression_function_bodies, lines_longer_than_80_chars, avoid_as, avoid_annotating_with_dynamic

mixin _$DiagnozeController on _DiagnozeController, Store {
  final _$busyAtom = Atom(name: '_DiagnozeController.busy');

  @override
  bool get busy {
    _$busyAtom.reportRead();
    return super.busy;
  }

  @override
  set busy(bool value) {
    _$busyAtom.reportWrite(value, super.busy, () {
      super.busy = value;
    });
  }

  final _$_DiagnozeControllerActionController =
      ActionController(name: '_DiagnozeController');

  @override
  void setBusy(bool value) {
    final _$actionInfo = _$_DiagnozeControllerActionController.startAction(
        name: '_DiagnozeController.setBusy');
    try {
      return super.setBusy(value);
    } finally {
      _$_DiagnozeControllerActionController.endAction(_$actionInfo);
    }
  }

  @override
  String toString() {
    return '''
busy: ${busy}
    ''';
  }
}
