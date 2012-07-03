
import alphasign

sign = alphasign.AlphaSign()
code = alphasign.AlphaCode()
sign.clear()
sign.setClock()
sign.setupMem()
sign.setSequence("abcdef")

style = code.Color(0) + code.Font(3)
sign.sendText(style + "America MURDERS", "a", "a")
sign.sendText(style + "America LIES", "a", "b")
sign.sendText(style + "America TORTURES", "a", "c")
sign.sendText(style + "America STEALS", "a", "d")
sign.sendText(style + "Our LEADERS are CRIMINALS", "a", "e")
sign.sendText(style + "GENOCIDE: 1,000,000 Iraqis are DEAD", "a", "f")
