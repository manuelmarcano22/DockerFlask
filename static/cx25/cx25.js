function downloadJSAtOnload() {
   JS9.Preload("static/cx25/cx25pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetPan(1650,600);
  JS9.SetZoom(2);
  JS9.SetScale('log',1000,10000);
  JS9.LoadRegions("static/cx25/cx25.reg");
  }
