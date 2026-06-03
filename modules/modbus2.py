def modbus_frame_process(
    inbox,
    outbox,
    modbus_frame_length,
    frame_process_status,
    slave_id,
    fun_code,
    input_reg,
    hold_reg,
    diagnostic_code,
    info_field
):
    crc1 = 0
    crc2 = 0
    temp = 0
    byte_count = 0
    fl_exception_code = 0

    # same VB logic here