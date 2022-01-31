var backgrounds = ["red", "green", "blue"];
function cb(item) {
	if($(item.target).is("a"))
        return true;

	item.colorIdx = item.colorIdx || 0;
    item.style.backgroundColor = backgrounds[item.colorIdx++ % backgrounds.length];
}