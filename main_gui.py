from tkinter import *
from tkinter import ttk
from tkintertable import TableCanvas
from instrument import Instrument


def run_gui(instrument: Instrument):
    root = Tk()
    root.title("Scope Setup")

    mainframe = ttk.Frame(root, width=1500, height=1500, padding=(20, 20, 20, 20))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # button selection code start

    btn_group = ttk.Frame(mainframe)
    btn_group.grid(column=0, row=0, sticky='NW')

    voltagelbl = ttk.Label(btn_group, text='Voltage level', background='white')
    sizelbl = ttk.Label(btn_group, text='Target Size', background='white')

    voltage = StringVar()
    size = StringVar()
    polarity = StringVar()

    small = ttk.Radiobutton(btn_group, text='Small', variable=size, value='small', command=lambda: instrument.set_size('small'))
    large = ttk.Radiobutton(btn_group, text='Large', variable=size, value='large', command=lambda: instrument.set_size('large'))

    pollbl = ttk.Label(btn_group, text='Polarity', background='white')
    pos = ttk.Radiobutton(btn_group, text='Positive', variable=polarity, value='positive', command=lambda: instrument.set_polarity_helper('positive'))
    neg = ttk.Radiobutton(btn_group, text='Negative', variable=polarity, value='negative', command=lambda: instrument.set_polarity_helper('negative'))

    v125 = ttk.Radiobutton(btn_group, text='125V', variable=voltage, value='125', command=lambda: instrument.set_voltage('500'))
    v250 = ttk.Radiobutton(btn_group, text='250V', variable=voltage, value='250', command=lambda: instrument.set_voltage('1000'))
    v500 = ttk.Radiobutton(btn_group, text='500V', variable=voltage, value='500', command=lambda: instrument.set_voltage('2000'))
    v750 = ttk.Radiobutton(btn_group, text='750V', variable=voltage, value='750', command=lambda: instrument.set_voltage('5000'))
    v1000 = ttk.Radiobutton(btn_group, text='1000V', variable=voltage, value='1000', command=lambda: instrument.set_voltage('10000'))

    sizelbl.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=(N, W), padx=5)
    small.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=(N, W), padx=5)
    large.grid(column=0, row=2, columnspan=1, rowspan=1, sticky=(N, W), padx=5)

    pollbl.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=(N, W), padx=5)
    pos.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=(N, W), padx=5)
    neg.grid(column=1, row=2, columnspan=1, rowspan=1, sticky=(N, W), padx=5)

    voltagelbl.grid(column=0, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=5)
    v125.grid(column=1, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=10)
    v250.grid(column=2, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=10)
    v500.grid(column=3, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=10)
    v750.grid(column=4, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=10)
    v1000.grid(column=5, row=4, columnspan=1, rowspan=1, sticky=(N, W), padx=10)

    btn_spacer = ttk.Label(btn_group, text='\t')
    btn_spacer.grid(column=0, row=3)

    # button selection code end

    # file group button code start

    file_group = ttk.Frame(mainframe)
    file_group.grid(column=0, row=1, sticky='W')

    check = ttk.Button(file_group, text='Check data', command=lambda: check_data(instrument, data, table))
    check.grid(column=0, row=0, padx=5, pady=5)

    copy = ttk.Button(file_group, text='Copy table', command=lambda: copy_table())
    copy.grid(column=1, row=0, padx=5, pady=5)

    # file group button code end

    # table code start

    table_frame = Frame(mainframe)
    table_frame.grid(column=0, row=2, padx=5, pady=20)

    data = {'small 125': {'Test': 'small 125V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'small 250': {'Test': 'small 250V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'small 500': {'Test': 'small 500V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'small 750': {'Test': 'small 750V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'small 1000': {'Test': 'small 1000V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'spacer': {'Test': None, 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'large 125': {'Test': 'large 125V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'large 250': {'Test': 'large 250V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'large 500': {'Test': 'large 500V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'large 750': {'Test': 'large 750V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None},
            'large 1000': {'Test': 'large 1000V', 'Ip1 (+)': None, 'Rise Time (+)': None, 'FWHM (+)': None, 'Undershoot (+)': None, 'Ip1 (-)': None, 'Rise Time (-)': None, 'FWHM (-)': None, 'Undershoot (-)': None}}

    table = TableCanvas(table_frame, data=data, rowheaderwidth=50, cellwidth=140, width=1250, height=220, thefont=('Arial', 12))
    table.show()

    # table code end

    # miscellaneous functions

    def fill_data(data_table, key, values_list, polarity):
        if key in data_table:
            if polarity == 'positive':
                keys_to_update = ['Ip1 (+)', 'Rise Time (+)', 'FWHM (+)', 'Undershoot (+)']
            elif polarity == 'negative':
                keys_to_update = ['Ip1 (-)', 'Rise Time (-)', 'FWHM (-)', 'Undershoot (-)']
            else:
                raise ValueError("Polarity must be 'positive' or 'negative'")

            for inner_key, value in zip(keys_to_update, values_list):
                data_table[key][inner_key] = value

    def check_data(instrument: Instrument, data_table: dict, table: TableCanvas):
        key = instrument.size + ' ' + instrument.voltage
        instrument.get_measurements()
        fill_data(data_table, key, [instrument.ip, instrument.tr, instrument.fwhm, instrument.ip2], instrument.polarity)

        data_range = {
            'small': {
                'voltage_range': {
                    '125': [1.4, 2.3],
                    '250': [2.9, 4.3],
                    '500': [6.1, 8.3],
                    '750': [9.2, 12.4],
                    '1000': [12.2, 16.5]
                },
                'time': 250.0,
                'fwhm': [250.0, 600.0],
                'undershoot': instrument.ip * 700
            },
            'large': {
                'voltage_range': {
                    '125': [2.3, 3.8],
                    '250': [4.8, 7.3],
                    '500': [10.3, 13.9],
                    '750': [15.5, 20.9],
                    '1000': [20.6, 27.9]
                },
                'time': 350.0,
                'fwhm': [450.0, 900.0],
                'undershoot': instrument.ip * 500
            }
        }

        false_position_column = []
        true_position_column = []

        if data_range[instrument.size]['voltage_range'][instrument.voltage][0] > instrument.ip or instrument.ip > data_range[instrument.size]['voltage_range'][instrument.voltage][1]:
            false_position_column.append(1)
        elif data_range[instrument.size]['voltage_range'][instrument.voltage][0] <= instrument.ip <= data_range[instrument.size]['voltage_range'][instrument.voltage][1]:
            true_position_column.append(1)

        if float(instrument.tr) > float(data_range[instrument.size]['time']):
            false_position_column.append(2)
        elif float(instrument.tr) <= float(data_range[instrument.size]['time']):
            true_position_column.append(2)

        if data_range[instrument.size]['fwhm'][0] > instrument.fwhm or instrument.fwhm > data_range[instrument.size]['fwhm'][1]:
            false_position_column.append(3)
        elif data_range[instrument.size]['fwhm'][0] <= instrument.fwhm <= data_range[instrument.size]['fwhm'][1]:
            true_position_column.append(3)

        if float(instrument.ip2) > float(data_range[instrument.size]['undershoot']):
            false_position_column.append(4)
        elif float(instrument.ip2) <= float(data_range[instrument.size]['undershoot']) / 2:
            true_position_column.append(4)

        if instrument.polarity == 'negative':
            false_position_column = [item + 4 for item in false_position_column]
            true_position_column = [item + 4 for item in true_position_column]

        key_position_row = list(data.keys()).index(key)
        for i in false_position_column:
            table.model.setColorAt(key_position_row, i, 'red')
        for i in true_position_column:
            table.model.setColorAt(key_position_row, i, 'white')
        table.redraw()

    def dict_to_tsv(data_dict):
        # Extract headers (column names) assuming all rows have the same structure
        headers = data_dict[next(iter(data_dict))].keys()
        tsv_string = "\t".join(headers) + "\n"  # Join headers with tab and add a newline

        # Iterate over the rows and their data
        for row_label, columns in data_dict.items():
            row_data = [str(columns[header]) for header in headers]
            tsv_string += "\t".join(row_data) + "\n"  # Join row data with tab and add a newline

        return tsv_string.strip()  # Remove the trailing newline

    def copy_table():
        root.clipboard_clear()
        root.clipboard_append(dict_to_tsv(data))

    root.eval('tk::PlaceWindow . center')
    root.mainloop()


if __name__ == "__main__":
    inst = Instrument()
    inst.connect()
    run_gui(inst)
