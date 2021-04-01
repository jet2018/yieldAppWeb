import 'package:flutter_modular/flutter_modular.dart';

Future navigateToPage(String page, {dynamic arguments}) async {
  await Modular.to.pushNamed(page, arguments: arguments);
}

Future navigateToPageAndRemoveAllPreviousPages(String page,
    {dynamic arguments}) async {
  await Modular.to
      .pushNamedAndRemoveUntil(page, (_) => false, arguments: arguments);
}
