import datetime


class FileLogger():

    def __init__(self, SUBJECT_NAME):
        import os
        directory = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(directory):
            os.makedirs(directory)

        d = datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        file_name = (SUBJECT_NAME + "_" +
                     # "BACK_" + str(BACKGROUND_PROFILE) + "_" +
                     # "DISK_" + str(DISKS_PROFILE) + "_" +
                    d + ".csv")
        file_path = os.path.join(directory, file_name)

        self.f = open(file_path, 'w')

        self.log_headers()

    def log_headers(self):

        str_store = ["KIND_OF_LOG","Date","trial_id","col1", "col2","col3","col4","col5","col6","col7","col8"]
        self.write_down(str_store)

        str_store = ["CLICK","Date","trial_id","box_clicked_num",
            "click_num","box_name","expected_box_name","time","correct","x","y"]
        self.write_down(str_store)

        str_store = ["RESULT","Date","trial_id","was_correct","number_of_box_clicked",
            "number_of_clicks", "expected_sequence", "result_sequence"]
        self.write_down(str_store)

        str_store = ["TRIAL START","Date","trial_id","sequence", "Feedback"]
        self.write_down(str_store)


    # def log_click(self, trial_id, box_clicked_num, click_num, box_name, expected_box_name, time, correct, x, y):
    #     str_store = []
    #     str_store.append("CLICK")
    #     str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
    #     str_store.append(str(trial_id))
    #     str_store.append(str(box_clicked_num))
    #     str_store.append(str(click_num))
    #     str_store.append(str(box_name))
    #     str_store.append(str(expected_box_name))
    #     str_store.append(str(time))
    #     str_store.append(str(correct))
    #     str_store.append(str(x))
    #     str_store.append(str(y))

    #     self.write_down(str_store)

    def log_trial_result(self, block_id, stim_kind, idx_trial, is_correct, time):
        str_store = []
        str_store.append("RESULT")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(block_id))
        str_store.append(str(stim_kind))
        str_store.append(str(idx_trial))
        str_store.append(str(is_correct))
        str_store.append(str(time))

        self.write_down(str_store)

    def log_trial_start(self, trial_id, source, target, feedback, expected_moves):
        str_store = []
        str_store.append("TRIAL START")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(trial_id))
        str_store.append(str(source))
        str_store.append(str(target))
        str_store.append(str(feedback))
        str_store.append(str(expected_moves))

        self.write_down(str_store)

    # def log_pick_disk(self, trial_id, source, target, current_board, move_num, picked_disk):
    #     str_store = []
    #     str_store.append("PICK DISK")
    #     str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
    #     str_store.append(str(trial_id))
    #     str_store.append(str(source))
    #     str_store.append(str(target))
    #     str_store.append(str(current_board))
    #     str_store.append(str(move_num))
    #     str_store.append(str(picked_disk))

    #     self.write_down(str_store)

    # def log_release_disk(self, trial_id, source, target, current_board, move_num, released_disk, new_position):
    #     str_store = []
    #     str_store.append("RELEASE DISK")
    #     str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
    #     str_store.append(str(trial_id))
    #     str_store.append(str(source))
    #     str_store.append(str(target))
    #     str_store.append(str(current_board))
    #     str_store.append(str(move_num))
    #     str_store.append(str(released_disk))
    #     str_store.append(str(new_position))

    #     self.write_down(str_store)


    def log_message(self, message):
        str_store = []
        str_store.append(message.upper())
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))

        self.write_down(str_store)

    def write_down(self, arr):
        str_store = ";".join(arr)
        # print "LOG ENTRY", str_store
        str_store = str_store + ";\n"
        self.f.write(str_store)

    def close(self):
        self.f.close()