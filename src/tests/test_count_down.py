from bpm_data_combiner.monitor_devices.bl.count_down import CountDown


def test_count_down():
    max_steps = 3
    cnt_dwn = CountDown(max_steps=max_steps)
    for cnt in range(max_steps):
        assert cnt_dwn.status()
        cnt_dwn.step()
    else:
        assert not cnt_dwn.status()

    cnt_dwn.step()
    assert not cnt_dwn.status()


def test_count_down_set_expired():
    cnt_dwn = CountDown(max_steps=42)
    assert cnt_dwn.status()
    cnt_dwn.set_expired()
    assert not cnt_dwn.status()