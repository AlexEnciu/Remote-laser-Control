Commands:
recipe->[Commant] [Target Motor Nr] [Value if is the case]

1. Move a relative Numbers of steps:
  Move X YYYYY
  ex: Move 0 2000
  
2. Move to an absolute value:
  MoveToAbs X YYYYY
  ex: MoveToAbs 0 1555

3. Move to homing possition:
  Homing X
  ex: Homing 0
  
4. Enable Motor
  Enable X
  ex: Enable 0
  
5. Disable Motor
  Disable X
  ex: Disable 0
  
6. Set the rotation direction
  Direction X YY [CW (clockwise), CCW (counter clockwise)]
  ex: Direction 0 CW

7. Read the status of the Motor
  ReadState X
  ex: ReadState 0 -> answear: ENABLE,CW

8. Read the absolute value stored in the counter
  ReadAbs X
  ex: ReadAbs 0
  
9. Set the rotation speed
  SetSpeed X YYYYY
  ex: SetSpeed 0 0.005 -> lower=faster
