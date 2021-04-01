import 'package:flutter/material.dart';
import 'package:yieldup/app/shared/global_variables.dart';

class CustomButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String title;
  final bool isBusy;
  final bool isActive;

  const CustomButton({
    Key key,
    @required this.title,
    @required this.onPressed,
    this.isBusy = false,
    this.isActive = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width * .8,
      child: FlatButton(
        disabledColor: disabledButtonColor,
        onPressed: isActive ? onPressed : null,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14.0),
          child: isBusy && isActive
              ? Container(
                  height: 20.0,
                  width: 20.0,
                  child: CircularProgressIndicator(
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  ),
                )
              : Opacity(
                  opacity: isActive ? 1 : 0.4,
                  child: Text(
                    title,
                    style: TextStyle(
                      color: Colors.white,
                      fontFamily: fontFamily,
                      fontSize: 14.0,
                    ),
                  ),
                ),
        ),
        color: isActive ? primaryColor : disabledButtonColor,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(
            buttonBorderRadius,
          ),
        ),
      ),
    );
  }
}

class CustomButtonWithoutColor extends StatelessWidget {
  final String title;
  final Color borderColor;
  final VoidCallback onPressed;
  final bool isBusy;

  CustomButtonWithoutColor({
    Key key,
    @required this.borderColor,
    @required this.title,
    @required this.onPressed,
    this.isBusy = false,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width * .8,
      child: FlatButton(
        onPressed: onPressed,
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 30.0,
            vertical: 16.0,
          ),
          child: isBusy
              ? Container(
                  height: 20.0,
                  width: 20.0,
                  child: CircularProgressIndicator(),
                )
              : Text(
                  title,
                  style: TextStyle(
                    color: borderColor,
                    fontFamily: fontFamily,
                    fontWeight: FontWeight.w600,
                    fontSize: 14.0,
                  ),
                ),
        ),
        shape: RoundedRectangleBorder(
          side: BorderSide(color: borderColor),
          borderRadius: BorderRadius.circular(
            buttonBorderRadius,
          ),
        ),
      ),
    );
  }
}

