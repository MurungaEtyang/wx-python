import wx
import json
from backend import generate_data, save_data_to_json
import os

class UserGenerator(wx.Frame):
    def __init__(self, parent, title):
        super(UserGenerator, self).__init__(parent, title=title, size=(1200, 700))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.search_bar = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.search_bar.SetForegroundColour(wx.Colour(128, 128, 128))
        self.search_bar.SetValue("Search users...")
        self.search_bar.Bind(wx.EVT_TEXT, self.on_search)
        self.search_bar.Bind(wx.EVT_SET_FOCUS, self.on_search_bar_focus)
        self.search_bar.Bind(wx.EVT_KILL_FOCUS, self.on_search_bar_kill_focus)
        vbox.Add(self.search_bar, 0, wx.EXPAND|wx.ALL, 10)

        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Campaign Name', width=250)
        self.list_ctrl.InsertColumn(1, 'Budget', width=100)
        self.list_ctrl.InsertColumn(2, 'Spent', width=100)
        self.list_ctrl.InsertColumn(3, 'Clicks', width=100)
        self.list_ctrl.InsertColumn(4, 'Impressions', width=100)
        self.list_ctrl.InsertColumn(5, 'User', width=200)
        vbox.Add(self.list_ctrl, 1, wx.EXPAND|wx.ALL, 20)

        self.btn_generate = wx.Button(self.panel, label='Generate Users', size=(200, 50))
        self.btn_generate.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        self.btn_generate.SetBackgroundColour('#4CAF50')
        self.btn_generate.SetForegroundColour(wx.WHITE)
        self.btn_generate.Bind(wx.EVT_BUTTON, self.on_generate_users)
        self.btn_generate.SetWindowStyleFlag(wx.BORDER_NONE)
        self.btn_generate.GetBestWidth(10)
        vbox.Add(self.btn_generate, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 20)

        self.panel.SetSizer(vbox)

        if os.path.exists('data.json'):
            self.load_and_display_data('data.json')

    def on_generate_users(self, event):
        with wx.BusyInfo("Generating data..."):
            data = generate_data()
            save_data_to_json(data)
        self.load_and_display_data('data.json')

    def load_and_display_data(self, filename):
        self.list_ctrl.DeleteAllItems()

        with open(filename, 'r') as file:
            data = json.load(file)

        for item in data:
            user = item['user']
            campaigns = item['campaigns']
            for campaign in campaigns:
                campaign_name = campaign['cmp_name']
                budget = str(campaign['cmp_bgt'])
                spent = str(campaign['cmp_spent'])
                clicks = str(campaign['cmp_clicks'])
                impressions = str(campaign['cmp_impr'])
                username = user['username']

                index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), campaign_name)
                self.list_ctrl.SetItem(index, 1, budget)
                self.list_ctrl.SetItem(index, 2, spent)
                self.list_ctrl.SetItem(index, 3, clicks)
                self.list_ctrl.SetItem(index, 4, impressions)
                self.list_ctrl.SetItem(index, 5, username)

    def on_search(self, event):
        query = self.search_bar.GetValue().lower()
        matching_indices = []
        non_matching_indices = []

        # Separate matching and non-matching indices
        for index in range(self.list_ctrl.GetItemCount()):
            username = self.list_ctrl.GetItemText(index, 5).lower()
            if query in username:
                matching_indices.append(index)
                self.list_ctrl.SetItemTextColour(index, wx.BLACK)
            else:
                non_matching_indices.append(index)
                self.list_ctrl.SetItemTextColour(index, wx.LIGHT_GREY)

        # Move matching items to the top
        for i, index in enumerate(matching_indices):
            if i != index:
                # Insert item at the correct position
                self.list_ctrl.InsertItem(i, self.list_ctrl.GetItemText(index, 0))
                for col in range(1, 6):
                    self.list_ctrl.SetItem(i, col, self.list_ctrl.GetItemText(index, col))
                # Remove the original item
                self.list_ctrl.DeleteItem(index - i)

        # Adjust indices for non-matching items
        for i, index in enumerate(non_matching_indices):
            self.list_ctrl.DeleteItem(index - len(matching_indices))

    def on_search_bar_focus(self, event):
        if self.search_bar.GetValue() == "Search users...":
            self.search_bar.SetValue("")
            self.search_bar.SetForegroundColour(wx.BLACK)

    def on_search_bar_kill_focus(self, event):
        if self.search_bar.GetValue() == "":
            self.search_bar.SetValue("Search users...")
            self.search_bar.SetForegroundColour(wx.Colour(128, 128, 128))

if __name__ == '__main__':
    app = wx.App()
    frame = UserGenerator(None, "User Generator")
    frame.Show()
    app.MainLoop()
