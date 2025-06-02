from flask import Blueprint,jsonify,request
from Controller import MissionPlannerController

mission_planner_routes = Blueprint('mission_planner_routes',__name__)

@mission_planner_routes.route('/insert_mission_plan',methods=['POST'])
def insert_mission_plan():
    data = request.get_json()
    mission_plan = MissionPlannerController.insert_mission_plan(data)
    if mission_plan:
        return jsonify({"success":True,'data':mission_plan}),200
    else:
        return jsonify({"success":False,'data':mission_plan}),400


@mission_planner_routes.route('/upload_mission_video', methods=['POST'])
def upload_mission_video():
    """
    API endpoint to upload and process mission videos
    """
    try:
        # Check if the post request has the file part
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        video = request.files['video']
        if video.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Get mission data
        mission_planner_id = request.form.get('mission_planner_id')
        if not mission_planner_id:
            return jsonify({"error": "Mission planner ID is required"}), 400

        # Process the data
        data = {"mission_planner_id": mission_planner_id}
        result = MissionPlannerController.insert_mission_video(data, video)

        if not result:
            return jsonify({"error": "Failed to process video"}), 500

        return jsonify({
            "success": True,
            "message": "Video processed successfully",
            "data": result
        }), 200

    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return jsonify({"error": str(e)}), 500


# @mission_planner_routes.route('/insert_mission_video',methods=['POST'])
# def insert_mission_video():
#     data = request.form.to_dict()
#     video = request.files.get('video')
#     mission_video = MissionPlannerController.insert_mission_video(data,video)
#     if mission_video:
#         return jsonify({"success":True,'data':mission_video}),200
#     else:
#         return jsonify({"success":False,'data':mission_video}),400

@mission_planner_routes.route('/update_mission_plan_by_id/<int:id>',methods=['PUT'])
def update_mission_plan_by_id(id):
    data = request.get_json()
    data['id'] = id
    mission_plan = MissionPlannerController.update_mission_plan_by_id(data)
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400

@mission_planner_routes.route('/get_all_mission_plans',methods=['GET'])
def get_all_mission_plans():
    mission_plans = MissionPlannerController.get_all_mission_plans()
    if mission_plans:
        return jsonify({'success':True,'data':mission_plans}),200
    else:
        return jsonify({'success':False,'data':mission_plans}),400

@mission_planner_routes.route('/get_mission_plan/<int:id>',methods=['GET'])
def get_mission_plan(id):
    mission_plan = MissionPlannerController.get_mission_plan_by_id(id)
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400

@mission_planner_routes.route('/delete_mission_plan_by_id/<int:id>',methods=['DELETE'])
def delete_mission_plan_by_id(id):
    mission_plan = MissionPlannerController.delete_mission_plan_by_id(id)
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400

@mission_planner_routes.route('/get_all_history',methods=['GET'])
def get_all_history():
    mission_plan = MissionPlannerController.get_all_history()
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400

@mission_planner_routes.route('/delete_history_by_id/<int:id>',methods=['DELETE'])
def delete_history_by_id(id):
    mission_plan = MissionPlannerController.delete_history_by_id(id)
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400

@mission_planner_routes.route('/update_mission_status_from_active_to_completed/<int:id>',methods=['PUT'])
def update_mission_status_from_active_to_completed(id):
    data = request.get_json()
    data['mission_planner_id'] = id
    mission_plan = MissionPlannerController.update_mission_status_from_active_to_completed(data)
    if mission_plan:
        return jsonify({'success':True,'data':mission_plan}),200
    else:
        return jsonify({'success':False,'data':mission_plan}),400