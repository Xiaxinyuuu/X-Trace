from pyecharts.charts import Line
import pyecharts.options as opts
import time

def Area():
    timelist = [0]
    numlist = [0]
    while True:
        i = yield
        times = i["times"]
        nums = i["nums"]
        timelist.append(times)
        numlist.append(nums)
        line = (
            Line(init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(animation=False)
            ))
            .add_xaxis(timelist)
            .add_yaxis("行人数量", numlist, is_smooth=True,
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color="skyblue"),
                       label_opts=opts.LabelOpts(is_show=False),
                       color='skyblue',
            )
            .render("person_counting.html")
        )
        time.sleep(0.1)

# if __name__ == '__main__':
#     Area()