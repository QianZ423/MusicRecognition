

from termcolor import colored


def print_error(message):
    '''
    打印错误信息
    :param message: 错误提示信息
    :return: None
    '''
    print(colored(message, 'red'))
    pass


def print_message(message):
    '''
    打印正常信息
    :param message: 正常提示信息
    :return: None
    '''
    print(colored(message, 'cyan'))
    pass


def print_warning(message):
    '''
    打印警告信息
    :param message: 警告提示信息
    :return: None
    '''
    print(colored(message, 'yellow'))
    pass







