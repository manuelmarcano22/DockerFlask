function downloadJSAtOnload() {
   JS9.Preload("static/cx25/cx25pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetZoom(0.3);
  JS9.SetScale('log',1000,100000);
  }
