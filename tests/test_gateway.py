import socket
import struct

from motor_fault.gateway import AlertOutput, ModbusServer, TagTable, modbus_read


def test_tags_follow_alert_and_clip_score():
    t = TagTable()
    t.update(True, True, 0.05)
    assert t.read(0, 4) == [1, 1, 32818, 1]
    t.update(False, False, -100.0)
    assert t.read(2, 1) == [0]
    assert t.read(3, 2) is None  # out of range


def test_modbus_roundtrip_and_errors():
    t = TagTable()
    srv = ModbusServer(t, port=0)
    srv.start()
    try:
        t.update(True, True, 0.0)
        assert modbus_read("127.0.0.1", srv.port, 0, 2) == [1, 1]
        try:
            modbus_read("127.0.0.1", srv.port, 3, 5)
            raise AssertionError("expected exception")
        except RuntimeError as e:
            assert "2" in str(e)
        with socket.create_connection(("127.0.0.1", srv.port), timeout=2) as s:  # unsupported function 6
            s.sendall(struct.pack(">HHHBBHH", 9, 0, 6, 1, 6, 0, 1))
            r = s.recv(9)
            assert r[7] == 0x86 and r[8] == 1
    finally:
        srv.stop()


def test_output_disabled_does_not_touch_gpio():
    o = AlertOutput(23, enabled=False)
    o.set(True)
    assert o.state is True
    o.release()
    assert o.state is False
