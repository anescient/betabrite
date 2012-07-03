
import alphasign

sign = alphasign.AlphaSign()
code = alphasign.AlphaCode()
sign.clear()
sign.setClock()
sign.setupMem()
sign.setSequence("aabcde")

style = code.Color(11) + code.Font(9)
sign.sendText(style + "Ron Paul 2008", "a", "a")

style = code.Color(0) + code.Font(12)
sign.sendText(style + "END THE WAR", "a", "b")

style = code.Color(0) + code.Font(3)
sign.sendText(style + "STOP THE TORTURE", "a", "c")
sign.sendText(style + "STOP THE LIES", "a", "d")

style = code.Color(2) + code.Font(6)
sign.sendText(style + "BRING OUR FAMILIES HOME", "a", "e")
