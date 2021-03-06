#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import time
import tensorflow as tf


class BenchmarkHook(tf.train.SessionRunHook):
    def __init__(self, steps, warmup_steps, log_steps, global_step_tensor, batch_size):
        self.steps = steps
        self.warmup_steps = warmup_steps
        self.log_steps = log_steps
        self.global_step_tensor = global_step_tensor
        self.batch_size = batch_size

        self.start_time = None
        self.last_time = None
        self.start_global_step = None
        self.benchmark_global_step = None
        self.benchmarking = False

    def before_run(self, run_context):
        return tf.train.SessionRunArgs(self.global_step_tensor)

    def after_run(self, run_context, run_values):
        current_global_step = run_values.results

        if self.start_global_step is None:
            self.start_global_step = current_global_step
            self.benchmark_global_step = self.start_global_step + self.warmup_steps
            print('B Starting warm up')
        elif current_global_step >= self.benchmark_global_step:
            if not self.benchmarking:
                print('B Done warm up')
                if self.log_steps != 0:
                    print('B Step\tutt/sec')
                self.last_time = self.start_time = time.time()
                self.benchmarking = True
            else:
                current_time = time.time()
                if self.log_steps != 0 and not (current_global_step - self.benchmark_global_step) % self.log_steps:
                    speed = self.log_steps * self.batch_size / (current_time - self.last_time)
                    self.last_time = current_time
                    print('B {}\t{:.2f}'.format(current_global_step - self.benchmark_global_step, speed))

                if current_global_step - self.benchmark_global_step == self.steps:
                    speed = self.steps * self.batch_size / (current_time - self.start_time)
                    print('-' * 64)
                    print('B total utt/sec: {:.2f}'.format(speed))
                    print('-' * 64)
                    run_context.request_stop()
def keep_only_digits(s):
    r'''
    local helper to just keep digits
    '''
    fs = ''
    for c in s:
        if c.isdigit():
            fs += c

    return int(fs)
