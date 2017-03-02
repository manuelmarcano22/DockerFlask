import sys
from pyraf import iraf
from astropy.io import fits

#To modify the center, low and high parameter
center = 100
low = -10.1
high = 50

#name of apfile
filename = 'database/apVI_SEXM_577734_2011-06-24T05_56_42.518_G475_MR_402230_Q4_hi' 
#name original SEXM
fitsfile1 = 'VI_SEXM_577734_2011-06-24T05:56:42.518_G475_MR_402230_Q4_hi.fits'
fitsfile1d = fits.open(fitsfile1)

#Exposure time to multiply the image
exptime = fitsfile1d[0].header['EXPTIME']
op = 'im1* '+str(exptime)
#
iraf.stsdas()
iraf.images.imutil()
iraf.images.imutil.imarith(fitsfile1, '*', exptime, 'cx25sexm.fits')

#Work with image
fitsfile = 'cx25sexm.fits'
fitsdata = fits.getdata(fitsfile)
#Default for dispesion line is half of the image
dispersion = fitsdata[:,fitsdata.shape[1]/2]
#create times the observing time

with open(filename) as f:
	for lines in f:
		if 'center' in lines:
	    		numerocenter = lines.split()[2]
		if 'low' in lines:
	    		numerolow = lines.split()[2]
		if 'high' in lines:
	    		numerohigh = lines.split()[2]
	    		break

with open(filename) as f:
	filedata = f.read()

filedata = filedata.replace(numerocenter,str(center))
filedata = filedata.replace(numerolow,str(low))
filedata = filedata.replace(numerohigh,str(high))

with open(filename,'w') as f:
	f.write(filedata)

#Call them 
iraf.noao.twodspec()
iraf.noao.twodspec.apextract()
#http://vivaldi.ll.iac.es/sieinvens/siepedia/pmwiki.php?n=HOWTOs.PythonianIRAF
iraf.noao.apextract.apall.setParam('input',fitsfile)

#iraf.noao.twodspec.apextract.apall.setParam('lower','-5.0')
#iraf.noao.twodspec.apextract.apall.setParam('upper','1.0')

iraf.noao.twodspec.apextract.apall.setParam('recenter','no')
iraf.noao.twodspec.apextract.apall.setParam('resize','no')
iraf.noao.twodspec.apextract.apall.setParam('edit','no')
iraf.noao.twodspec.apextract.apall.setParam('trace','no')
iraf.noao.twodspec.apextract.apall.setParam('interactive','no')
iraf.noao.twodspec.apextract.apall.setParam('upper','1.0')
iraf.noao.twodspec.apextract.apall.setParam('apertures','1')
iraf.noao.twodspec.apextract.apall.setParam('find','no')
iraf.noao.apextract.apall.saveParList(filename='cx25.par')
iraf.noao.twodspec.apextract.apall(ParList='cx25.par')
