function downloadJSAtOnload() {
   JS9.Preload("static/cx970/cx970pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetPan(1025,1416);
  JS9.SetZoom(0.25);
  JS9.SetScale('log',1000,200000);
  JS9.LoadRegions("static/cx970/cx970.reg");
  }
