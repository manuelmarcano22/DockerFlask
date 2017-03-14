function downloadJSAtOnload() {
   JS9.Preload("static/cx183/cx183pre.fits",{scale:'log',onload: func})
 }
  if (window.addEventListener)
      window.addEventListener("load", downloadJSAtOnload, false);
  else if (window.attachEvent)
      window.attachEvent("onload", downloadJSAtOnload);
  else window.onload = downloadJSAtOnload;
  function func() {
  JS9.SetPan(1248,1293);
  JS9.SetZoom(2);
  JS9.SetScale('log',100,1000000);
  JS9.LoadRegions("static/cx183/cx183.reg");
  }
