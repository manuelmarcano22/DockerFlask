function downloadJSAtOnload() {
   JS9.Preload("static/cx59/cx59pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetPan(1000,1000);
  JS9.SetZoom(.3);
  JS9.SetScale('log',1000,10000);
  JS9.LoadRegions("static/cx59/cx59.reg");
  }
