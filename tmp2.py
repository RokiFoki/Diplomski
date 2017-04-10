import re

line = '<img src="nekaj" class="nekaj2" title="nekaj3">'
line = r'(112471, \'widget_log\', \'Player\', datetime.datetime(2016, 11, 14, 14, 11, 9, 843000), \'{"lesson":"224","widget":"1020","logDetails":{"time":10.471,"gameLog":[{"tile1":{"id":1,"pairId":2,"type":"image","url":"img/data-likovi/11kocka.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/11kocka.jpg" class="innerPic">"},"tile2":{"id":2,"pairId":1,"type":"image","url":"img/data-likovi/12kocka.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/12kocka.jpg" class="innerPic">"},"correct":true},{"tile1":{"id":5,"pairId":6,"type":"image","url":"img/data-likovi/31kugla.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/31kugla.jpg" class="innerPic">"},"tile2":{"id":6,"pairId":5,"type":"image","url":"img/data-likovi/32kugla.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/32kugla.jpg" class="innerPic">"},"correct":true},{"tile1":{"id":7,"pairId":8,"type":"image","url":"img/data-likovi/41valjak.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/41valjak.jpg" class="innerPic">"},"tile2":{"id":8,"pairId":7,"type":"image","url":"img/data-likovi/42valjak.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/42valjak.jpg" class="innerPic">"},"correct":true},{"tile1":{"id":9,"pairId":10,"type":"image","url":"img/data-likovi/51piramida.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/51piramida.jpg" class="innerPic">"},"tile2":{"id":12,"pairId":11,"type":"image","url":"img/data-likovi/62stozac.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/62stozac.jpg" class="innerPic">"},"correct":false},{"tile1":{"id":10,"pairId":9,"type":"image","url":"img/data-likovi/52piramida.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/52piramida.jpg" class="innerPic">"},"tile2":{"id":9,"pairId":10,"type":"image","url":"img/data-likovi/51piramida.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/51piramida.jpg" class="innerPic">"},"correct":true},{"tile1":{"id":3,"pairId":4,"type":"image","url":"img/data-likovi/21kvadar.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/21kvadar.jpg" class="innerPic">"},"tile2":{"id":4,"pairId":3,"type":"image","url":"img/data-likovi/22kvadar.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/22kvadar.jpg" class="innerPic">"},"correct":true},{"tile1":{"id":12,"pairId":11,"type":"image","url":"img/data-likovi/62stozac.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/62stozac.jpg" class="innerPic">"},"tile2":{"id":11,"pairId":12,"type":"image","url":"img/data-likovi/61stozac.jpg","selected":true,"htmlSnippet":"<img src="img/data-likovi/61stozac.jpg" class="innerPic">"},"correct":true}]}}\', 2879936)'
print("line:{}".format(line))


regex = r'(.*)<img([^>]+)([^\\>])"(.*)'
regex = r'(.*)<img([^>]+)([^\\>])"(.*)'

ct = r'\1<img\2\3\"\4'

m = re.search(regex, line)
k = 0
while m:
	print(line)
	line = re.sub(regex, ct, line)
	
	m = re.search(regex, line)
	
	k += 1

print(line)

print(k)
"""
if m:
	print(m.groups())
else:
	print("NO!")
"""