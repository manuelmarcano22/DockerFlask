function downloadJSAtOnload() {
   JS9.Preload("static/cx191/cx191pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetPan(1000,1000);
  JS9.SetZoom(.2);
  //JS9.SetScale('log',1000,10000);
  JS9.SetScale('squared',1000,10000);
  JS9.LoadRegions("static/cx191/cx191.reg");
  }
