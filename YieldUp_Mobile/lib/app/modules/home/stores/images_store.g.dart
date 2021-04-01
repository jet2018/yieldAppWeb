// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'images_store.dart';

// **************************************************************************
// StoreGenerator
// **************************************************************************

// ignore_for_file: non_constant_identifier_names, unnecessary_brace_in_string_interps, unnecessary_lambdas, prefer_expression_function_bodies, lines_longer_than_80_chars, avoid_as, avoid_annotating_with_dynamic

mixin _$ImagesStore on _ImagesStore, Store {
  final _$errorAtom = Atom(name: '_ImagesStore.error');

  @override
  String get error {
    _$errorAtom.reportRead();
    return super.error;
  }

  @override
  set error(String value) {
    _$errorAtom.reportWrite(value, super.error, () {
      super.error = value;
    });
  }

  final _$resultAtom = Atom(name: '_ImagesStore.result');

  @override
  DiagnosisResult get result {
    _$resultAtom.reportRead();
    return super.result;
  }

  @override
  set result(DiagnosisResult value) {
    _$resultAtom.reportWrite(value, super.result, () {
      super.result = value;
    });
  }

  final _$selectedImageAtom = Atom(name: '_ImagesStore.selectedImage');

  @override
  File get selectedImage {
    _$selectedImageAtom.reportRead();
    return super.selectedImage;
  }

  @override
  set selectedImage(File value) {
    _$selectedImageAtom.reportWrite(value, super.selectedImage, () {
      super.selectedImage = value;
    });
  }

  final _$_ImagesStoreActionController = ActionController(name: '_ImagesStore');

  @override
  void setError(String error) {
    final _$actionInfo = _$_ImagesStoreActionController.startAction(
        name: '_ImagesStore.setError');
    try {
      return super.setError(error);
    } finally {
      _$_ImagesStoreActionController.endAction(_$actionInfo);
    }
  }

  @override
  void setResult(DiagnosisResult result) {
    final _$actionInfo = _$_ImagesStoreActionController.startAction(
        name: '_ImagesStore.setResult');
    try {
      return super.setResult(result);
    } finally {
      _$_ImagesStoreActionController.endAction(_$actionInfo);
    }
  }

  @override
  void setSelectedImage(File image) {
    final _$actionInfo = _$_ImagesStoreActionController.startAction(
        name: '_ImagesStore.setSelectedImage');
    try {
      return super.setSelectedImage(image);
    } finally {
      _$_ImagesStoreActionController.endAction(_$actionInfo);
    }
  }

  @override
  String toString() {
    return '''
error: ${error},
result: ${result},
selectedImage: ${selectedImage}
    ''';
  }
}
