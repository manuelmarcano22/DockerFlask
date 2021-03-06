var click;
if( "ontouchstart" in document.documentElement ){
  click = "touchstart";
} else {
  click = "click";
}
$(".zoom").on(click, function(evt){
  var s = $(evt.currentTarget).attr("id");
  JS9.SetZoom(s.charAt(1));
  return false;
});

$(".zoomuno").on(click, function(evt){
  JS9.SetPan(628,1866);
  JS9.SetZoom(2);
  return false;
});

$(".zoomdos").on(click, function(evt){
  JS9.SetPan(836,2052);
  JS9.SetZoom(4);
  return false;
});

$(".zoomtres").on(click, function(evt){
  JS9.SetPan(1200,1899);
  JS9.SetZoom(8);
  return false;
});

$(".zoomcuatro").on(click, function(evt){
  JS9.SetPan(1784,804);
  JS9.SetZoom(4);
  return false;
});

$(".zoom2").on(click, function(evt){
  var s = $(evt.currentTarget).attr("id");
  var s2 = "|1"
  JS9.SetZoom(s.concat(s2));
  return false;
});

$(".scale").on(click, function(evt){
  var s = $(evt.currentTarget).attr("id");
  JS9.SetScale(s);
  return false;
});
$(".color").on(click, function(evt){
  var s = $(evt.currentTarget).attr("id");
  JS9.SetColormap(s);
  return false;
});
$(".region").on(click, function(evt){
  var s = $(evt.currentTarget).attr("id");
  JS9.AddRegions(s);
  return false;
});
JS9.Panner.HTML = "";
