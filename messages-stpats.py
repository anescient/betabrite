
import alphasign

sign = alphasign.AlphaSign()
code = alphasign.AlphaCode()
sign.clear()
sign.setClock()
sign.setupMem()
sign.setSequence("abcde")

style = code.Color(1) + code.Font(4)
sign.sendText( style + "St. Pat's 2008", "nC", "a" )

style = code.Color(1) + code.Font(5)
sign.sendText( style + "St. Pat's", "o", "b" )

style = code.Color(9) + code.Font(7)
sign.sendText( style + "100", "nZ", "c" )

style = code.Color(8) + code.Font(7)
sign.sendText( style + "100", "n0", "d" )

style = code.Color(8) + code.Font(3)
sign.sendText( style + "HIGH SCORE", "n5", "e" )

