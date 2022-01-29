def create_response_obj(success, status, data):
  return {
    "success": success,
    "status": status,
    "data": {
      "result": data
    }
  }


def check_table_tracker_existence(table_name, mapper):
  flag = True
  message = None
  tracker = None
  
  tracker = mapper.get(table_name, None)
  if not tracker:
    message = f"Tracker is not defined for the table '{table_name}'"
    flag = False
  
  return flag, tracker, message
