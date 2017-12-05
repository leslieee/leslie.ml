#coding:utf-8
from django.utils.safestring import mark_safe


def page(baseurl, totalnum, currentpage):
    perpage = 20
    pagenum = 11

    temp = divmod(totalnum, perpage)

    totalpage = temp[0]
    if temp[1]:
        totalpage += 1


    start = 1
    if currentpage>6:
         start = currentpage - 5
    end = currentpage + 5

    if end > totalpage:
        end = totalpage


    html = []
    for i in range(start, end):
        url = baseurl + str(i)
        if i == currentpage:
            html.append('<a class="selected" href="'+url+'">' + str(i) + '</a>')
        else:
            html.append('<a href="'+url+'">'+str(i)+'</a>')

    return mark_safe(''.join(html))
