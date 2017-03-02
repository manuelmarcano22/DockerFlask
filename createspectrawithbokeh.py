from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show, curdoc
from bokeh.resources import CDN
from bokeh.embed import autoload_static
from bokeh.models import HoverTool, tools, ColumnDataSource, CustomJS, Slider
from bokeh.layouts import  column
from astropy.io import fits
from astropy.convolution import convolve, Box1DKernel
import numpy as np

#Get data
srfm = fits.open('VI_SRFM_577734_2011-06-24T05:56:42.518_G475_MR_402230_Q4_hi.fits')
secondstar = srfm[0].data[1]

#For srfm[0].header["CTYPE1"] = 'LINEAR'
xn = srfm[0].header["NAXIS1"]
refx = srfm[0].header["CRVAL1"]
step = srfm[0].header['CD1_1']
cr = srfm[0].header['CRPIX1']

xlist = [ refx + step*(i - cr) for i in np.arange(1, len(secondstar)+1) ]

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

layout = column(slider, plot)
output_file(name+'try.html')
show(layout)

#create html and js for standalone
#Js is a js file that provides data for the plot and the tag is the tag to include in the html document.
#js, tag = autoload_static(plot, CDN, "{{site.baseurl}}/images/bokehgraphs/"+name+".js")
js, tag = autoload_static(layout, CDN, "{{site.baseurl}}/images/bokehgraphs/"+name+".js")

##To save it in files

with open(name+'.js','w') as jsfile:
	jsfile.write(js)

with open(name+'.html','w') as htmlfile:
	htmlfile.write(tag)
