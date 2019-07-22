import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GLib



from urllib import request

stock_list = [
    "sh000001",  # 上证指数
    "sz002157",  # 正邦科技
    "sz002124",  # 天邦股份
    "sz002714",  # 牧原股份
    "sz002567",  # 唐人神
    "sz000876",  # 新希望
    "sh600975",  # 新五丰
]

display_filed_list = "代码 名称 涨幅 今开 昨收 当前".split(' ')

FIELD_INDEX_DICT = {
    "代码": 0,
    "名称": 1,
    "今开": 2,
    "昨收": 3,
    "当前": 4,
    "最高": 5,
    "最低": 6,
    "竞买": 7,  # 买一
    "竞卖": 8,  # 卖一
    "成交数": 9,  # 通常把该值除以一百
    "成交金额": 10,  # 通常把该值除以一万
    "日期": -4,
    "时间": -3,
    "涨幅": -1
}



class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="gtk stock")
        self.set_border_width(5)
        self.set_default_size(400, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(self.box)

        #Creating the ListStore model
        self.liststore = Gtk.ListStore(*[str]*len(display_filed_list))

        #creating the treeview, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.liststore)
        for i, column_title in enumerate(display_filed_list):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sort_column_id(i)
            self.treeview.append_column(column)

        #setting up the layout, putting the treeview in a scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_min_content_width(400)
        self.scrollable_treelist.set_min_content_height(400)
        
        self.box.pack_start(self.scrollable_treelist, True, True, 0)
        self.scrollable_treelist.add(self.treeview)
        self.treeview.connect("cursor-changed", self.__toggle_row)

        self.image = Gtk.Image()
        self.box.pack_start(self.image, True, True, 0)

        self.refresh_data(None)
        self.show_image()
        GLib.timeout_add_seconds(10, self.refresh_data, None)
        self.show_all()

    def __toggle_row(self, tree_view):
        path, column = tree_view.get_cursor()
        treeiter = self.liststore.get_iter(path)
        value = self.liststore.get_value(treeiter, 0)
        self.show_image(value)

    def show_image(self, stock_code='sh000001'):
        url = "http://image.sinajs.cn/newchart/min/n/{stock_code}.gif".format(stock_code=stock_code)
        response = request.urlopen(url)
        data = response.read()
        pixbuf_loader = GdkPixbuf.PixbufLoader.new()
        pixbuf_loader.write(data)
        pixbuf = pixbuf_loader.get_pixbuf()
        self.image.set_from_pixbuf(pixbuf)
        pixbuf_loader.close()

    def refresh_data(self, args):
        url = "http://hq.sinajs.cn/?format=text&list=" + ','.join(stock_list)
        
        with request.urlopen(url) as f:
            data = f.read().decode('gb18030')
        data = data.replace('=', ',')
        line_list = data.splitlines()

        self.liststore.clear()
        for line in line_list:
            field_list = line.split(',')
            field_list.append(str(round((float(field_list[4])-float(field_list[3]))/float(field_list[3]) * 100, 2 ))) # 涨幅
            stock_field_list = []
            for name in display_filed_list:
                try:
                    value = round(float(field_list[FIELD_INDEX_DICT[name]]), 2)
                    stock_field_list.append(str(value))
                except ValueError:
                    stock_field_list.append(field_list[FIELD_INDEX_DICT[name]])
            self.liststore.append(stock_field_list)


if __name__ == '__main__':
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
