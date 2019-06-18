from Info_getter.MsgPublisher import MsgPublisher


def run():
    '''
    主程序入口
    :return:
    '''
    MsgPublisher().run()


def test_run():
    '''
    运行前的测试
    :return:
    '''
    MsgPublisher().start_today_info(is_test=True)

if __name__ == '__main__':
    # test_run()
    run()



