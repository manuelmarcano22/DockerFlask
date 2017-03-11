from flask import Flask
import flask
import sys
import os
import optparse
import time
from bokeh.util.string import encode_utf8
from astropy.io import fits
from stsci.tools import capable
capable.OF_GRAPHICS = False
from pyraf import iraf
from bokeh.plotting import figure, output_file
from bokeh.io import output_file, show, curdoc, show
from bokeh.resources import CDN, INLINE
from bokeh.embed import autoload_static, components
from bokeh.models import HoverTool, tools, ColumnDataSource, CustomJS, Slider
from bokeh.layouts import  column, row
from astropy.convolution import convolve, Box1DKernel
import numpy as np
from shutil import copyfile

app = Flask(__name__)

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

start = int(round(time.time()))

# Temporary
#fitsfile1 = 'static/cx25/cx25.fits'
#fitsfile1d = fits.open(fitsfile1)
##Exposure time to multiply the image
#exptime = fitsfile1d[0].header['EXPTIME']
#op = 'im1* '+str(exptime)
#iraf.stsdas()
#iraf.images.imutil()
#iraf.images.imutil.imarith(fitsfile1, '*', exptime, 'cx25sexm.fits')






#app
@app.route("/")
def polynomial():
    """ Very simple embedding of a polynomial chart
    """
    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    center = int(getitem(args, 'center', 100))
    low = int(getitem(args, 'low',-10.1 ))
    high = int(getitem(args, 'high', 50))

    ##---- begin spectracx25.py ----#
    #
    ##To modify the center, low and high parameter
#    center = 100
#    low = -10.1
#    high = 50
    #
    ##name of apfile
    #I am not sure if I need to do this
    if os.path.exists('cx25sexm.ms.fits'):
        os.rename('cx25sexm.ms.fits','cx25sexm.msrecent.fits')
        os.remove('cx25sexm.fits')

    if not os.path.exists('database'):
        os.makedirs('database')
        os.makedirs('uparm')
    #filename = 'static/cx25/database/apcx25sexm' 
    filename = 'database/apcx25sexm' 
    copyfile('static/cx25/database/apcx25sexm',filename)
    copyfile('static/cx25/twcapextt.par','uparm/twcapextt.par')
    ###name original SEXM
    ##fitsfile1 = 'VI_SEXM_577734_2011-06-24T05:56:42.518_G475_MR_402230_Q4_hi.fits'
    fitsfile1 = 'static/cx25/cx25.fits'
    fitsfile1d = fits.open(fitsfile1)
    #
    ###Exposure time to multiply the image
    exptime = fitsfile1d[0].header['EXPTIME']
    op = 'im1* '+str(exptime)
    ###
    iraf.stsdas()
    iraf.images.imutil()
    #iraf.images.imutil.imarith(fitsfile1, '*', exptime, 'static/cx25/cx25sexm.fits')
    iraf.images.imutil.imarith(fitsfile1, '*', exptime, 'cx25sexm.fits')
    ##
    ###Work with image
    #fitsfile = 'static/cx25/cx25sexm.fits'
    fitsfile = 'cx25sexm.fits'
    fitsdata = fits.getdata(fitsfile)
    ###Default for dispesion line is half of the image
    dispersion = fitsdata[:,fitsdata.shape[1]/2]
    ###create times the observing time
    ##
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
    #try output
    iraf.noao.apextract.apall.setParam('output','cx25sexm.ms.fits')
    #
    ##iraf.noao.twodspec.apextract.apall.setParam('lower','-5.0')
    ##iraf.noao.twodspec.apextract.apall.setParam('upper','1.0')
    #
    iraf.noao.twodspec.apextract.apall.setParam('recenter','no')
    iraf.noao.twodspec.apextract.apall.setParam('resize','no')
    iraf.noao.twodspec.apextract.apall.setParam('edit','no')
    iraf.noao.twodspec.apextract.apall.setParam('trace','no')
    iraf.noao.twodspec.apextract.apall.setParam('interactive','no')
    iraf.noao.twodspec.apextract.apall.setParam('upper','1.0')
    iraf.noao.twodspec.apextract.apall.setParam('apertures','1')
    iraf.noao.twodspec.apextract.apall.setParam('find','no')
    #iraf.noao.apextract.apall.saveParList(filename='static/cx25/cx25.par')
    #iraf.noao.twodspec.apextract.apall(ParList='static/cx25/cx25.par')
    iraf.noao.apextract.apall.saveParList(filename='uparm/cx25.par')
    iraf.noao.twodspec.apextract.apall(ParList='uparm/cx25.par')
    ###### end spectracx25.py



    #########begin createpsectrawithbokeh.py 
    ##Get data
    #I am not usre if I need this. 
    if not os.path.exists('cx25sexm.msrecent.fits'):
        srfm = fits.open('static/cx25/cx25sexm.ms.fits')
    srfm = fits.open('cx25sexm.ms.fits')
    secondstar = srfm[0].data
    #
    ##For srfm[0].header["CTYPE1"] = 'LINEAR'
    xn = srfm[0].header["NAXIS1"]
    refx = srfm[0].header["CRVAL1"]
    step = srfm[0].header['CD1_1']
    cr = srfm[0].header['CRPIX1']
    #
    xlist = [ refx + step*(i - cr) for i in np.arange(1, len(secondstar)+1) ]
    #
    name = 'spectraap3cx25smoothsky'

    hover = HoverTool(
            tooltips=[
                ("index", "$index"),
                ("(x,y)", "($x{1}, $y)"),
            ]
        )

    #Create ColumnDataSource
    x = np.array(xlist)
    y = np.array(secondstar)
    #Create y for each smooth. Need to fix this
    ysmooth3 = convolve(y, Box1DKernel(3))
    ysmooth5 = convolve(y, Box1DKernel(5))

    source = ColumnDataSource(data=dict(x=x,y=y))
    source3 = ColumnDataSource(data=dict(x=x,y=ysmooth3))
    source5 = ColumnDataSource(data=dict(x=x,y=ysmooth5))

    plot = figure(x_axis_label='Angstrom', y_axis_label='Y')
    plot.add_tools(hover)
    plot.add_tools(tools.ResizeTool())
    #Eraaseplot.line(xlist,secondstar)
    plot.line('x','y',source=source)

    ##Callback in JS
    callback = CustomJS(args=dict(source=source,source3=source3,source5=source5), code="""
            var data = source.data;
            var data3 = source3.data;
            var data5 = source5.data;
            var f = cb_obj.value
            y = data['y']
            y3 = data3['y']
            y5 = data5['y']
            
            if (f == 3.0){
            for (i = 0; i < y.length; i++) {
                y[i] = y3[i]
            }
            }
            
            if (f == 5.0){
            for (i = 0; i < y.length; i++) {
                y[i] = y5[i]
            }
            }
            source.trigger('change');
        """)


    #Set up slider
    slider = Slider(title="Smooth Curve", value=1.0, start=1.0, end=5.0, step=2.0,callback=callback)

# #Set aperture
    ape = fits.open('cx25sexm.fits')
    ape = ape[0].data
    #Default is half
    y = ape[:,int(ape.shape[1]/2)]
    x = list(range(y.shape[0]))
    c2 = figure(x_axis_label='abc')
    c2.line(x,y)

    p = row(plot,c2)
    
    #layout = column(slider, plot)
    layout = column(slider, p)


#    output_file(name+'try.html')
#    show(layout)
#
#    #create html and js for standalone
#    #Js is a js file that provides data for the plot and the tag is the tag to include in the html document.
#    #js, tag = autoload_static(plot, CDN, "{{site.baseurl}}/images/bokehgraphs/"+name+".js")
#    js, tag = autoload_static(layout, CDN, "{{site.baseurl}}/images/bokehgraphs/"+name+".js")
#
#    ##To save it in files
#
#    with open(name+'.js','w') as jsfile:
#            jsfile.write(js)
#
#    with open(name+'.html','w') as htmlfile:
#            htmlfile.write(tag)
#
#    ##### end createpsectrawithbokeh.py 


#    # Create a polynomial line graph with those arguments
#    x = list(range(_from, to + 1))
#    fig = figure(title="Polynomial")
#    fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(layout)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        center=center,
        high=high,
        low=low
    )
    return encode_utf8(html)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python simpleapp.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.debug = True
    #app.run(host='grades.manuelpm.me',port=int(args.port), debug=False)
    app.run(host='127.0.0.1',port=int(args.port), debug=False)
