extends CharacterBody2D
const SPEED = 100.0
const SPEED_ROTATE = 40
const SPEED_ROTATE_TOWER = 80
const JUMP_VELOCITY = -400.0

@onready var _body_animated = $Sprite/Body_Animated
@onready var _tower_animated = $Sprite/Tower_Animated

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var rotation_angle = 0;
var animation_body;
var animation_tower;
var rotation_tower_degrees = 0;
#var rotation_tower_degrees_modulate = 0;
#var rotation_degrees_modulate = 0;

func _on_ready():
	pass

func _physics_process(delta):
	# Add the gravity.
	#if not is_on_floor():
		#velocity.y += gravity * delta
		#
	var rotate = Input.get_axis("ui_left", "ui_right")
	var rotate_tower = Input.get_axis("ui_left", "ui_right")
	var direction_y = Input.get_axis("ui_up", "ui_down")
	if rotate:
		rotation_degrees += rotate * SPEED_ROTATE * delta
	#if rotation_degrees < 0:
		#rotation_degrees_modulate = rotation_degrees + 360
	#else if rotation_degrees > 360:
		#rotation_degrees_modulate = rotation_degrees
		
	if rotate_tower:
		rotation_tower_degrees += rotate_tower * SPEED_ROTATE_TOWER * delta
		if rotation_tower_degrees < -180:
			rotation_tower_degrees += 360
		if rotation_tower_degrees > 180:
			rotation_tower_degrees -= 360
		#if rotation_tower_degrees < 0:
			#rotation_tower_degrees_modulate = rotation_tower_degrees + 360
		#else:
			#rotation_degrees_modulate = rotation_tower_degrees
	#print(rotate, ",  ", SPEED_ROTATE, ",  ", delta, ",  ", rotate_tower, ",  ", SPEED_ROTATE_TOWER, ",  ", delta, ",  ", rotation_degrees, ",  ", rotation_tower_degrees)

	if direction_y:
		velocity.y = direction_y * SPEED
	else:
		velocity.y = move_toward(velocity.y, 0, SPEED)
		
	# Using move_and_slide.
	move_and_slide()
	
	
	#for i in get_slide_collision_count():
		#var collision = get_slide_collision(i)
		#print("I collided with ", collision.get_collider().name)

func _process(delta):
	#pass
	if rotation_degrees:
		animation_body = (rotation_degrees) / 6
		animation_body = snapped(animation_body, 1)
		if animation_body < 0:
			animation_body +=60
		if animation_body == 60:
			animation_body = 0
		_body_animated.set_rotation(animation_body * -6)
		_body_animated.set_frame_and_progress(animation_body, 1)
		
	if rotation_tower_degrees || rotation_degrees:
		animation_tower = (rotation_tower_degrees + rotation_degrees) / 6
		animation_tower = snapped(animation_tower, 1)
		if animation_tower > 60:
			animation_tower -=60
			if animation_tower > 60:
				animation_tower -=60
		if animation_tower < 0:
			animation_tower +=60
			if animation_tower < 0:
				animation_tower +=60
		if animation_tower == 60:
			animation_tower = 0
		_tower_animated.set_rotation(animation_tower * -6 + rotation_tower_degrees)
		_tower_animated.set_frame_and_progress(animation_tower, 1)
		print(animation_body, ",  ", rotation_tower_degrees, ",  ", rotation_degrees,)

selected_tag:t=""
bin_dump_file:t=""

mission_settings{
  atmosphere{
    pressure:r=760
    temperature:r=15
  }

  player{
    army:i=1
    wing:t="t1_player01"
  }

  player_teamB{
    army:i=2
  }

  mission{
    name:t="norway_helicopter_mission_attack"
    type:t="singleMission"
    level:t="levels/EasternEurope22.bin"
    campaign:t="RideR2"
    chapter:t="Helicopters"
    restoreType:t="manual"
    optionalTakeOff:b=no
    missionDebriefing:t=""
    missionBriefing:t=""
    environment:t="Day"
    weather:t="cloudy"
    locName:t="[Norway] AH-1G"
    forceSkiesInitialRandomSeed:b=yes
    skiesInitialRandomSeed:i=487080
    windSpeed:p2=4, 12
    windDirectionDeg:p2=240, 310
    isPreciseCollisionDetectionEnabled:b=yes

    missionType{
      _Dom:b=no
      _Conq:b=no
      _CnvA:b=no
      _CnvB:b=no
      _ArtDA:b=no
      _ArtDB:b=no
      _Bttl:b=no
      _DBttlA:b=no
      _DBttlB:b=no
      _Bto:b=no
      _Flc:b=no
      _v1_race_straight:b=no
      _v1_race_inverted:b=no
      _v2_race_straight:b=no
      _v2_race_inverted:b=no
      _Conq1:b=no
      _Conq2:b=no
      _Conq3:b=no
      _Conq4:b=no
      _Conq5:b=no
      _Conq6:b=no
    }

    tags{
    }
  }

  spectator_points{
  }

  cover_points{
  }

  aiParams{
    aiEffectivenessViscosity:r=90
    effectivenessDistances:p2=2500, 7000
  }
}

imports{
}

triggers{
  isCategory:b=yes
  is_enabled:b=yes

  mission_init{
    is_enabled:b=yes
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      initMission{
      }
    }

    conditions{
    }

    actions{
      comment{
        value:t="add an airfield and spawn the player"
      }

      addAirfield{
        runwayStart:t="t1_helipad_area_01"
        runwayEnd:t="t1_helipad_area_02"
        runwayWidth:r=400
        army:i=1
        spawnPoint:t="t1_helipad_spawn_01"
        spawnPoint:t="t1_helipad_spawn_02"
        spawnPoint:t="t1_helipad_spawn_03"
        visibleOnHud:b=no
      }

      spawnOnAirfield{
        runwayName:t="t1_helipad01"
        objects:t="t1_player01"
      }

      comment{
        value:t="airfield icon"
      }

      missionShowMapIcon{
        show:b=yes
        iconName:t="ui/gameuiskin#objective_helicopter"
        areaName:t="airfield_marker"
        colorCode:t="Team A"
      }

      comment{
        value:t="set battlearea"
      }

      missionBattleArea{
        air:b=yes
        ground:b=no
        mapArea:b=yes
        killArea:b=no
        detectionArea:b=yes
        killOutOfBattleArea:b=yes
        newGridHorizontalCellCount:i=0
        area:t="mission_battlearea_01"
        area:t="mission_battlearea_02"
        area:t="mission_battlearea_03"
        area:t="mission_battlearea_04"
        area:t="mission_battlearea_05"
        area:t="mission_battlearea_06"
        area:t="mission_battlearea_07"
        area:t="mission_battlearea_08"
        area:t="mission_battlearea_09"
        area:t="mission_battlearea_10"
        team:t="Both"
      }

      comment{
        value:t="some useless actions for the airfield"
      }

      airfieldSetIndication{
        set:b=no
        target:t="t1_helipad01"
        team:t="Both"
      }

      airfieldSetProperties{
        object:t="t1_helipad01"
        repair_mul:r=10
        fuel_mul:r=1
        reload_mul:r=4
        "enemySurrenderOnLanding ":b=yes
      }

      comment{
        value:t="disable useless units"
      }

      unitPutToSleep{
        target:t="t2_boat_02"
        target:t="t1_heli_bot02"
      }

      unitPutToSleep{
        target:t="gunboat_squad_01"
      }

      comment{
        value:t="random numbers for killing ground units"
      }

      varSetRandomInt{
        var:t="inf_number_to_kill_int_01"
        from:i=5
        to_not_including:i=10
      }

      varSetRandomInt{
        var:t="inf_number_to_kill_int_02"
        from:i=10
        to_not_including:i=15
      }

      varSetRandomInt{
        var:t="veh_number_to_kill_int"
        from:i=2
        to_not_including:i=3
      }

      varSetRandomInt{
        var:t="veh_number_to_kill_int_02"
        from:i=4
        to_not_including:i=6
      }

      varSetRandomInt{
        var:t="inf_sec_number_to_kill_int_01"
        from:i=7
        to_not_including:i=15
      }

      varSetRandomInt{
        var:t="veh_sec_number_to_kill_int_01"
        from:i=3
        to_not_including:i=4
      }

      comment{
        value:t="mark for spotting"
      }

      unitMark{
        target_marking:i=1
        target:t="aaa_effi_squad"
        target:t="all_enemy_units_squad"
      }

      comment{
        value:t="enable first objective trigger and waypoint"
      }

      triggerEnable{
        target:t="takeoff_waypoint"
        target:t="cutscene"
        target:t="heli_bot_settings"
        target:t="secondary_objective_01"
      }

      comment{
        value:t="set move stand for all units - panic trigger"
      }

      triggerEnable{
        target:t="panic_stand"
      }

      comment{
        value:t="enable panic triggers"
      }

      triggerEnable{
        target:t="player_when_shot_01"
        target:t="player_when_shot_02"
        target:t="player_when_shot_03"
      }
    }

    else_actions{
    }
  }

  cutscene{
    is_enabled:b=yes
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      initMission{
      }
    }

    conditions{
    }

    actions{
      comment{
        value:t="disable player controls"
      }

      playerControls{
        setStatus:t="disable"
        control:t="ALL"
      }

      comment{
        value:t="cutscene objects - set to be ignored by AI"
      }

      unitSetProperties{
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        object:t="cutscene_02"
        object:t="cutscene_01"
        object:t="cutscene_03"
        object:t="cutscene_04"
        object:t="cutscene_05"
        object:t="cutscene_06"
        targetableByAi:b=no
        stealthRadius:r=0
        ignoresEnemy:b=yes
      }

      comment{
        value:t="start cutscene"
      }

      missionStartCutscene{
        target:t="cutscene_01"
        second_target:t="cutscene_02"
        duration:r=4
        camera_type:t="two_obj"
        direction_amp:r=1
        flat_offs:p3=100, 100, 100
        zoom:r=1.4
        frequency:r=1
        linear_at_vel:p3=0, 0, 0
        linear_eye_vel:p3=0, 0, 0
        linear_at_accel:r=0
        linear_eye_accel:r=0
        linear_relative:b=no
        pitch:r=0.1
        yaw:r=0
        pitch_amplitude:r=1
        yaw_amplitude:r=1
        distance:r=30
        shake_mult:r=0
        splineEye:t=""
        splineAt:t=""
        splineSpeed:r=100
        resetCamera:b=yes
        shake_accel:r=0
        fov_accel:r=0
        mustHaveGui:b=no
        beginFade:p2=0, 2
        endFade:p2=0, 0
        delayPlayer:b=no
      }

      showCutsceneInfo{
        text:t="Autumn 1968"
        duration:r=2
      }

      wait{
        time:r=3
      }

      showCutsceneInfo{
        text:t="Enemy forces have been spotted in the nearby area next to the port"
        duration:r=5
      }

      wait{
        time:r=1
      }

      missionStartCutscene{
        target:t="cutscene_03"
        second_target:t="cutscene_04"
        duration:r=4
        camera_type:t="two_obj"
        direction_amp:r=1
        flat_offs:p3=100, 100, 100
        zoom:r=2.5
        frequency:r=1
        linear_at_vel:p3=0, 0, 0
        linear_eye_vel:p3=0, 0, 0
        linear_at_accel:r=0
        linear_eye_accel:r=0
        linear_relative:b=no
        pitch:r=0.1
        yaw:r=0
        pitch_amplitude:r=1
        yaw_amplitude:r=1
        distance:r=30
        shake_mult:r=0
        splineEye:t=""
        splineAt:t=""
        splineSpeed:r=100
        resetCamera:b=yes
        shake_accel:r=0
        fov_accel:r=0
        mustHaveGui:b=no
        beginFade:p2=0, 0
        endFade:p2=0, 0
        delayPlayer:b=no
      }

      missionStartCutscene{
        target:t="cutscene_05"
        second_target:t="cutscene_06"
        duration:r=4
        camera_type:t="flat_linear"
        direction_amp:r=1
        flat_offs:p3=100, 100, 100
        zoom:r=2.5
        frequency:r=1
        linear_at_vel:p3=2, 5, 2
        linear_eye_vel:p3=2, 5, 2
        linear_at_accel:r=0
        linear_eye_accel:r=0
        linear_relative:b=no
        pitch:r=0.1
        yaw:r=0
        pitch_amplitude:r=1
        yaw_amplitude:r=1
        distance:r=30
        shake_mult:r=0
        splineEye:t=""
        splineAt:t=""
        splineSpeed:r=100
        resetCamera:b=no
        shake_accel:r=0
        fov_accel:r=0
        mustHaveGui:b=no
        linear_at:p3=500, 0, 0
        linear_eye:p3=0.01, 0, 0
        beginFade:p2=0, 0
        endFade:p2=0, 0
        delayPlayer:b=no
      }

      wait{
        time:r=4
      }

      missionStartCutscene{
        target:t="cutscene_05"
        second_target:t="cutscene_06"
        duration:r=4
        camera_type:t="two_obj"
        direction_amp:r=1
        flat_offs:p3=100, 100, 100
        zoom:r=2.5
        frequency:r=1
        linear_at_vel:p3=0, 0, 0
        linear_eye_vel:p3=0, 0, 0
        linear_at_accel:r=0
        linear_eye_accel:r=0
        linear_relative:b=no
        pitch:r=0.1
        yaw:r=0
        pitch_amplitude:r=1
        yaw_amplitude:r=1
        distance:r=30
        shake_mult:r=0
        splineEye:t=""
        splineAt:t=""
        splineSpeed:r=100
        resetCamera:b=yes
        shake_accel:r=0
        fov_accel:r=0.3
        mustHaveGui:b=no
        beginFade:p2=0, 0
        endFade:p2=0, 0
        delayPlayer:b=no
      }

      missionStartCutscene{
        target:t="cutscene_03"
        second_target:t="cutscene_04"
        duration:r=4
        camera_type:t="flat_linear"
        direction_amp:r=1
        flat_offs:p3=100, 100, 100
        zoom:r=2.5
        frequency:r=1
        linear_at_vel:p3=-50, -50, -50
        linear_eye_vel:p3=-50, -50, -50
        linear_at_accel:r=0
        linear_eye_accel:r=0
        linear_relative:b=no
        pitch:r=0.1
        yaw:r=0
        pitch_amplitude:r=1
        yaw_amplitude:r=1
        distance:r=30
        shake_mult:r=0
        splineEye:t=""
        splineAt:t=""
        splineSpeed:r=100
        resetCamera:b=no
        shake_accel:r=0
        fov_accel:r=0
        mustHaveGui:b=no
        linear_at:p3=0, 0, 0
        linear_eye:p3=50, 50, 50
        beginFade:p2=0, 0
        endFade:p2=3, 4
        delayPlayer:b=no
      }

      showCutsceneInfo{
        text:t="Your task is to find and destroy them"
        duration:r=4
      }

      wait{
        time:r=4
      }

      showCutsceneInfo{
        text:t="Good luck"
        duration:r=3
      }

      comment{
        value:t="end cutscene"
      }

      wait{
        time:r=1
      }

      comment{
        value:t="put to sleep cutscene objects"
      }

      unitPutToSleep{
        target:t="cutscene_03"
        target:t="cutscene_04"
        target:t="cutscene_02"
        target:t="cutscene_01"
        target:t="cutscene_05"
        target:t="cutscene_06"
      }

      comment{
        value:t="set fuel"
      }

      unitSetProperties{
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        object:t="t1_player01"
        fuel:r=40
      }

      comment{
        value:t="enable player controls"
      }

      playerControls{
        setStatus:t="enable"
        control:t="ALL"
      }
    }

    else_actions{
    }
  }

  takeoff_waypoint{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
    }

    actions{
      comment{
        value:t="add first waypoints. objectives and set variables"
      }

      moAddMissionObjective{
        target:t="norway_helicopter_mission_attack_obj_01"
      }

      missionMarkAsWaypoint{
        visible:b=no
        primary:b=yes
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="@first_waypoint_string_01"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=no
        primary:b=no
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="@second_waypoint_string_01"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=yes
        primary:b=yes
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="waypoint_01_01"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=yes
        primary:b=no
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="waypoint_01_02"
        team:t="Both"
      }

      varSetString{
        value:t="waypoint_01_01"
        var:t="first_waypoint_string_01"
      }

      varSetString{
        value:t="waypoint_01_02"
        var:t="second_waypoint_string_01"
      }

      varSetString{
        value:t="waypoint_01_"
        var:t="waypoint_name_var"
      }

      triggerEnable{
        target:t="waypoint_follow"
      }
    }

    else_actions{
    }
  }

  takeoff_waypoint_no_obj{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
    }

    actions{
      comment{
        value:t="add first waypoints and set variables"
      }

      missionMarkAsWaypoint{
        visible:b=no
        primary:b=yes
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="@first_waypoint_string_01"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=no
        primary:b=no
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="@second_waypoint_string_01"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=yes
        primary:b=yes
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="waypoint_01_08"
        team:t="Both"
      }

      missionMarkAsWaypoint{
        visible:b=yes
        primary:b=no
        oriented:b=no
        ignoreDifficulty:b=yes
        scale:r=0.3
        target:t="waypoint_01_09"
        team:t="Both"
      }

      varSetString{
        value:t="waypoint_01_08"
        var:t="first_waypoint_string_01"
      }

      varSetString{
        value:t="waypoint_01_09"
        var:t="second_waypoint_string_01"
      }

      varSetString{
        value:t="waypoint_01_"
        var:t="waypoint_name_var"
      }

      triggerEnable{
        target:t="waypoint_follow_no_obj"
      }
    }

    else_actions{
    }
  }

  waypoint_follow{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
      unitWhenInArea{
        math:t="3D"
        object_type:t="isAlive"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        check_objects:t="any"
        object:t="t1_player01"
        target:t="@first_waypoint_string_01"
      }
    }

    actions{
      moSetObjectiveStatus{
        target:t="norway_helicopter_mission_attack_obj_01"
        status:i=2
      }

      triggerEnable{
        target:t="load_first_w"
      }

      moAddMissionObjective{
        target:t="norway_helicopter_mission_attack_obj_02"
      }

      wait{
        time:r=10
      }

      playHint{
        hintType:t="standard"
        name:t="Fly at very low altitude to not be detected by the enemy SPAA units"
        action:t="show"
        shouldFadeOut:b=yes
        isOverFade:b=yes
        time:r=10
        priority:i=1
        target_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
      }
    }

    else_actions{
    }
  }

  waypoint_follow_no_obj{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
      unitWhenInArea{
        math:t="3D"
        object_type:t="isAlive"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        check_objects:t="any"
        object:t="t1_player01"
        target:t="@first_waypoint_string_01"
      }
    }

    actions{
      triggerEnable{
        target:t="load_first_w"
      }
    }

    else_actions{
    }
  }

  heli_bot_settings{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=no
    }

    events{
      periodicEvent{
        time:r=0.3
      }
    }

    conditions{
    }

    actions{
      missionKillEffects{
        area:t="t1_helipad_spawn_02"
        area:t="t1_helipad_spawn_01"
        effect:b=yes
        bullets:b=yes
        rockets:b=yes
        bombs:b=yes
        torpedoes:b=yes
      }

      unitSetProperties{
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        object:t="t1_heli_bot01"
        object:t="t1_heli_bot02"
        cannotMove:b=yes
        aiEnabled:b=no
        enginesEnabled:b=no
        takeoffPermission:b=no
        fuel:r=0
        stayOnGround:b=yes
      }

      unitDoBailout{
        object:t="t1_heli_bot01"
        object:t="t1_heli_bot02"
      }

      spawnOnAirfield{
        runwayName:t="t1_helipad01"
        objects:t="t1_heli_bot01"
      }

      unitDoBailout{
        object:t="t1_heli_bot01"
        object:t="t1_heli_bot02"
      }
    }

    else_actions{
    }
  }

  check_player_alt{
    isCategory:b=yes
    is_enabled:b=yes

    if_above_01{
      isCategory:b=yes
      is_enabled:b=yes

      if_above_01_first{
        is_enabled:b=yes
        comments:t=""

        props{
          actionsType:t="PERFORM_ONE_BY_ONE"
          conditionsType:t="ALL"
          enableAfterComplete:b=yes
        }

        events{
          periodicEvent{
            time:r=1
          }
        }

        conditions{
          unitWhenReachHeight{
            object_type:t="isAlive"
            object_marking:i=0
            check_objects:t="all"
            value:r=0
            comparasion_func:t="more"
            absolute_value:b=no
            object:t="t1_player01"
          }

          unitWhenReachHeight{
            object_type:t="isAlive"
            object_marking:i=0
            check_objects:t="all"
            value:r=75
            comparasion_func:t="less"
            absolute_value:b=no
            object:t="t1_player01"
          }
        }

        actions{
          varSetInt{
            value:i=1
            var:t="check_player_alt_var_int"
          }

          triggerEnable{
            target:t="if_above_01_change"
          }
        }

        else_actions{
        }
      }

      if_above_01_change{
        is_enabled:b=no
        comments:t=""

        props{
          actionsType:t="PERFORM_ONE_BY_ONE"
          conditionsType:t="ALL"
          enableAfterComplete:b=no
        }

        events{
          periodicEvent{
            time:r=1
          }
        }

        conditions{
          unitWhenStatus{
            object_type:t="isMarked"
            check_objects:t="any"
            object_marking:i=1
            object_var_name:t=""
            object_var_comp_op:t="equal"
            object_var_value:i=0
            target_type:t="isAlive"
            check_period:r=1
            object:t="aaa_effi_squad"
          }
        }

        actions{
          unitSetProperties{
            object_marking:i=0
            object_var_name:t=""
            object_var_comp_op:t="equal"
            object_var_value:i=0
            object:t="aaa_effi_squad"
            useForTriggerFiltered:b=yes
            attack_type:t="dont_aim"
            accuracy:r=0
            effShootingRate:r=0
            airEffShootingRate:r=0
            fireRandom:b=yes
            targetChangeInterval:r=1
            targetChangeProf:r=0.25
          }
        }

        else_actions{
        }
      }
    }

    if_above_02{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=75
          comparasion_func:t="more"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=80
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }
      }

      actions{
        varSetInt{
          value:i=2
          var:t="check_player_alt_var_int"
        }

        triggerEnable{
          target:t="if_above_02_change"
        }
      }

      else_actions{
      }
    }

    if_above_02_change{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isMarked"
          check_objects:t="any"
          object_marking:i=1
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="aaa_effi_squad"
        }
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          useForTriggerFiltered:b=yes
          attack_type:t="fire_at_will"
          accuracy:r=0.3
          checkVisibilityTarget:b=yes
          effShootingRate:r=0.3
          airEffShootingRate:r=0.3
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
      }
    }

    if_above_03{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=80
          comparasion_func:t="more"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=128
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }
      }

      actions{
        varSetInt{
          value:i=3
          var:t="check_player_alt_var_int"
        }

        triggerEnable{
          target:t="if_above_03_change"
        }
      }

      else_actions{
      }
    }

    if_above_03_change{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isMarked"
          check_objects:t="any"
          object_marking:i=1
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="aaa_effi_squad"
        }
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          useForTriggerFiltered:b=yes
          attack_type:t="fire_at_will"
          accuracy:r=0.4
          checkVisibilityTarget:b=yes
          effShootingRate:r=0.3
          airEffShootingRate:r=0.3
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
      }
    }

    if_above_04{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=128
          comparasion_func:t="more"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=256
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }
      }

      actions{
        varSetInt{
          value:i=4
          var:t="check_player_alt_var_int"
        }

        triggerEnable{
          target:t="if_above_04_change"
        }
      }

      else_actions{
      }
    }

    if_above_04_change{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isMarked"
          check_objects:t="any"
          object_marking:i=1
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="aaa_effi_squad"
        }
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          useForTriggerFiltered:b=yes
          attack_type:t="fire_at_will"
          accuracy:r=0.5
          checkVisibilityTarget:b=yes
          effShootingRate:r=0.5
          airEffShootingRate:r=0.5
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
      }
    }

    if_above_05{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=256
          comparasion_func:t="more"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=512
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }
      }

      actions{
        varSetInt{
          value:i=5
          var:t="check_player_alt_var_int"
        }

        triggerEnable{
          target:t="if_above_05_change"
        }
      }

      else_actions{
      }
    }

    if_above_05_change{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isMarked"
          check_objects:t="any"
          object_marking:i=1
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="aaa_effi_squad"
        }
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          useForTriggerFiltered:b=yes
          attack_type:t="fire_at_will"
          accuracy:r=0.7
          checkVisibilityTarget:b=yes
          effShootingRate:r=0.8
          airEffShootingRate:r=0.8
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
      }
    }

    if_above_06{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=512
          comparasion_func:t="more"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=2048
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }
      }

      actions{
        varSetInt{
          value:i=6
          var:t="check_player_alt_var_int"
        }

        triggerEnable{
          target:t="if_above_06_change"
        }
      }

      else_actions{
      }
    }

    if_above_06_change{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isMarked"
          check_objects:t="any"
          object_marking:i=1
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="aaa_effi_squad"
        }
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          useForTriggerFiltered:b=yes
          attack_type:t="fire_at_will"
          accuracy:r=1
          checkVisibilityTarget:b=yes
          effShootingRate:r=1
          airEffShootingRate:r=1
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
      }
    }

    when_in_spot_area_01{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="all_spot_area_01"
          target:t="all_spot_area_02"
          target:t="all_spot_area_03"
          target:t="all_spot_area_04"
          target:t="all_spot_area_05"
          target:t="all_spot_area_06"
          target:t="all_spot_area_07"
          target:t="all_spot_area_08"
        }
      }

      actions{
        triggerDisable{
          target:t="if_above_01_first"
          target:t="if_above_02"
          target:t="if_above_03"
          target:t="if_above_04"
          target:t="if_above_05"
          target:t="if_above_06"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="aaa_effi_squad"
          attack_type:t="fire_at_will"
          accuracy:r=0.5
          effShootingRate:r=0.5
          airEffShootingRate:r=0.5
          fireRandom:b=yes
          targetChangeInterval:r=1
          targetChangeProf:r=0.25
        }
      }

      else_actions{
        triggerEnable{
          target:t="if_above_01_first"
          target:t="if_above_02"
          target:t="if_above_03"
          target:t="if_above_04"
          target:t="if_above_05"
          target:t="if_above_06"
        }
      }
    }

    when_in_spot_area_02{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="boat_fire_area"
          target:t="boat_fire_area01"
          target:t="boat_fire_area02"
        }
      }

      actions{
        unitMark{
          target_marking:i=3
          target:t="t2_boat_01"
          target:t="t2_boat_02"
          target:t="t2_boat_03"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t2_boat_01"
          object:t="t2_boat_02"
          object:t="t2_boat_03"
          stealthRadius:r=2000
          forceVisibleOnMap:b=yes
          attack_type:t="fire_at_will"
          checkVisibilityTarget:b=yes
        }

        wait{
          time:r=5
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t2_boat_01"
          object:t="t2_boat_02"
          object:t="t2_boat_03"
          stealthRadius:r=200
          forceVisibleOnMap:b=no
          attack_type:t="return_fire"
        }

        unitMark{
          target_marking:i=1
          target:t="t2_boat_01"
          target:t="t2_boat_02"
          target:t="t2_boat_03"
        }
      }

      else_actions{
      }
    }
  }

  show_hint_spa_nearby{
    is_enabled:b=yes
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=yes
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
      unitDistanceBetween{
        value:r=3000
        math:t="3D"
        object_type:t="isAlive"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        target_type:t="isAlive"
        target_marking:i=0
        check_objects:t="any"
        check_targets:t="any"
        object:t="t1_player01"
        target:t="aaa_effi_squad"
        check_all_units:b=yes
      }

      varCompareInt{
        var_value:t="check_player_alt_var_int"
        value:i=1
        comparasion_func:t="more"
      }
    }

    actions{
      playHint{
        hintType:t="standard"
        name:t="STAY AT LOW ALT"
        action:t="show"
        shouldFadeOut:b=no
        isOverFade:b=no
        time:r=1
        priority:i=0
        target_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        shouldBlink:b=yes
        useForTriggerFiltered:b=yes
        team:t="A"
      }
    }

    else_actions{
    }
  }

  load_waypoints{
    isCategory:b=yes
    is_enabled:b=yes

    load_first_w{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="@first_waypoint_string_01"
        }
      }

      actions{
        missionMarkAsWaypoint{
          visible:b=no
          primary:b=yes
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="@first_waypoint_string_01"
          team:t="Both"
        }

        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="@second_waypoint_string_01"
          team:t="Both"
        }

        varSetString{
          value:t=""
          var:t="first_waypoint_string_01"
          input_var:t="waypoint_name_var"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="first_waypoint_int_01"
        }

        varAddString{
          value:t=""
          digits:i=2
          var:t="first_waypoint_string_01"
          input_var:t="first_waypoint_int_01"
        }

        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=yes
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="@first_waypoint_string_01"
          team:t="Both"
        }

        triggerEnable{
          target:t="load_second_w"
        }
      }

      else_actions{
      }
    }

    load_second_w{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        objectExists{
          target:t="@first_waypoint_string_01"
          type:t="area"
        }
      }

      actions{
        varSetString{
          value:t=""
          var:t="second_waypoint_string_01"
          input_var:t="waypoint_name_var"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="second_waypoint_int_01"
        }

        varAddString{
          value:t=""
          digits:i=2
          var:t="second_waypoint_string_01"
          input_var:t="second_waypoint_int_01"
        }

        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="@second_waypoint_string_01"
          team:t="Both"
        }

        triggerEnable{
          target:t="load_first_w"
        }
      }

      else_actions{
        triggerEnable{
          target:t="@last_waypoint_trigger_string_01"
        }

        moSetObjectiveStatus{
          target:t="norway_helicopter_mission_attack_obj_02"
          status:i=2
        }

        triggerDisable{
          target:t="load_first_w"
          target:t="load_second_w"
        }
      }
    }

    debug{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
      }

      actions{
        playHint{
          hintType:t="standard"
          name:t="@first_waypoint_string_01"
          action:t="show"
          shouldFadeOut:b=no
          isOverFade:b=no
          time:r=-1
          priority:i=0
          target_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
        }
      }

      else_actions{
      }
    }
  }

  spotting{
    isCategory:b=yes
    is_enabled:b=yes

    set{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
      }

      actions{
        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
          object:t="t1_ground_units_squad"
          stealthRadius:r=50
        }
      }

      else_actions{
      }
    }

    when_hit{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ANY"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="isShooting"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
        }

        unitWhenStatus{
          object_type:t="hittedBy"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
          hittedByTarget:t="t1_squad"
        }

        unitDistanceBetween{
          value:r=300
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          target_marking:i=0
          check_objects:t="any"
          check_targets:t="any"
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
          target:t="t1_player01"
          compareCenters:b=yes
          check_all_units:b=yes
        }
      }

      actions{
        unitMark{
          target_marking:i=3
          target:t="all_enemy_units_squad"
          target:t="gunboat_squad_01"
          useForTriggerFiltered:b=yes
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
          useForTriggerFiltered:b=yes
          stealthRadius:r=2000
          forceVisibleOnMap:b=yes
          checkVisibilityTarget:b=yes
        }

        wait{
          time:r=10
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="all_enemy_units_squad"
          object:t="gunboat_squad_01"
          useForTriggerFiltered:b=yes
          stealthRadius:r=200
          forceVisibleOnMap:b=no
        }

        unitMark{
          target_marking:i=1
          target:t="all_enemy_units_squad"
          target:t="gunboat_squad_01"
          useForTriggerFiltered:b=yes
        }
      }

      else_actions{
      }
    }

    when_hit_hit{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ANY"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenStatus{
          object_type:t="hittedBy"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="all_enemy_units_squad"
          hittedByTarget:t="t1_squad"
        }

        unitDistanceBetween{
          value:r=300
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          target_marking:i=0
          check_objects:t="any"
          check_targets:t="any"
          object:t="all_enemy_units_squad"
          target:t="t1_player01"
          compareCenters:b=yes
          check_all_units:b=yes
        }
      }

      actions{
        unitMark{
          target_marking:i=3
          target:t="all_enemy_units_squad"
          useForTriggerFiltered:b=yes
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="all_enemy_units_squad"
          useForTriggerFiltered:b=yes
          stealthRadius:r=2000
          forceVisibleOnMap:b=yes
          attack_type:t="fire_at_will"
          checkVisibilityTarget:b=yes
        }

        wait{
          time:r=5
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="all_enemy_units_squad"
          useForTriggerFiltered:b=yes
          stealthRadius:r=200
          forceVisibleOnMap:b=no
          attack_type:t="return_fire"
        }

        unitMark{
          target_marking:i=1
          target:t="all_enemy_units_squad"
          useForTriggerFiltered:b=yes
        }
      }

      else_actions{
      }
    }
  }

  spaa_when_hit{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ANY"
      enableAfterComplete:b=yes
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
      unitWhenStatus{
        object_type:t="hittedBy"
        check_objects:t="any"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        target_type:t="isAlive"
        check_period:r=1
        object:t="aaa_effi_squad"
        hittedByTarget:t="t1_player01"
      }

      unitDistanceBetween{
        value:r=30
        math:t="2D"
        object_type:t="isAlive"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        target_type:t="isAlive"
        target_marking:i=0
        check_objects:t="any"
        check_targets:t="any"
        object:t="t1_player01"
        target:t="aaa_effi_squad"
        compareCenters:b=yes
        check_all_units:b=yes
      }
    }

    actions{
      unitMark{
        target_marking:i=2
        target:t="aaa_effi_squad"
        useForTriggerFiltered:b=yes
      }

      unitSetProperties{
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        object:t="aaa_effi_squad"
        useForTriggerFiltered:b=yes
        accuracy:r=0.4
        effShootingRate:r=0.4
        airEffShootingRate:r=0.4
      }

      wait{
        time:r=5
      }

      unitMark{
        target_marking:i=1
        target:t="aaa_effi_squad"
        useForTriggerFiltered:b=yes
      }
    }

    else_actions{
    }
  }

  panic_player_in_area{
    isCategory:b=yes
    is_enabled:b=yes

    panic_stand{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=0.01
        }
      }

      conditions{
      }

      actions{
        unitMoveTo{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target:t="player_shot_area_01"
          target_marking:i=0
          waypointReachedDist:r=10
          recalculatePathDist:r=-1
          follow_target:b=no
          teleportHeightType:t="absolute"
          useUnitHeightForTele:b=yes
          shouldKeepFormation:b=no
          teleportHeightValue:r=1000
          horizontalDirectionForTeleport:b=yes
          object:t="panic_squad_01"
          move_type:t="stand"
        }

        unitMoveTo{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target:t="player_shot_area_02"
          target_marking:i=0
          waypointReachedDist:r=10
          recalculatePathDist:r=-1
          follow_target:b=no
          teleportHeightType:t="absolute"
          useUnitHeightForTele:b=yes
          shouldKeepFormation:b=no
          teleportHeightValue:r=1000
          horizontalDirectionForTeleport:b=yes
          object:t="panic_squad_02"
          move_type:t="stand"
        }

        unitMoveTo{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target:t="player_shot_area_03"
          target_marking:i=0
          waypointReachedDist:r=10
          recalculatePathDist:r=-1
          follow_target:b=no
          teleportHeightType:t="absolute"
          useUnitHeightForTele:b=yes
          shouldKeepFormation:b=no
          teleportHeightValue:r=1000
          horizontalDirectionForTeleport:b=yes
          object:t="panic_squad_03"
          move_type:t="stand"
        }
      }

      else_actions{
      }
    }

    player_when_shot_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isShooting"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="player_shot_area_01"
        }
      }

      actions{
        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_01"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 5
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_01"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 4
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_01"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 3
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_01"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 2
        }
      }

      else_actions{
      }
    }

    player_when_shot_02{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isShooting"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="player_shot_area_02"
        }
      }

      actions{
        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_02"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 5
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_02"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 4
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_02"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 3
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_02"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 2
        }
      }

      else_actions{
      }
    }

    player_when_shot_03{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isShooting"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="player_shot_area_03"
        }
      }

      actions{
        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_03"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 5
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_03"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 4
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_03"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 3
        }

        wait{
          time:r=1
        }

        unitFollowWaypoints{
          followWaypoints:b=yes
          target:t="panic_squad_03"
          resetWaypoints:b=yes
          randomTargetsCount:i=8
          delayForObjects:p2=1, 2
        }
      }

      else_actions{
      }
    }
  }

  objectives{
    isCategory:b=yes
    is_enabled:b=yes

    destroy_enemy_units_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="simulator"
          is:t="equal"
        }
      }

      actions{
        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_03"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t2_destroy_target_01"
          object:t="t2_infantry_squad_01"
        }

        unitSetIndication{
          target_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          set:b=yes
          target:t="t2_destroy_target_01"
          target:t="t2_infantry_squad_01"
          target_type:t="isAlive"
          team:t="Both"
        }

        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="enemy_waypoint_01"
          target:t="enemy_waypoint_02"
          team:t="Both"
        }

        varSetInt{
          value:i=0
          var:t="inf_number_to_kill_int_both"
          input_var:t="inf_number_to_kill_int_01"
        }

        varSetInt{
          value:i=0
          var:t="veh_number_to_kill_int_both"
          input_var:t="veh_number_to_kill_int"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="inf_number_to_kill_int_both"
          use_variable:b=yes
          var_value:t="inf_number_to_kill_int_02"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="veh_number_to_kill_int_both"
          use_variable:b=yes
          var_value:t="veh_number_to_kill_int_02"
        }

        triggerEnable{
          target:t="destroy_enemy_units_02"
          target:t="destroy_enemy_units_a"
          target:t="destroy_enemy_units_b"
        }
      }

      else_actions{
        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_03"
        }

        unitSetIndication{
          target_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          set:b=yes
          target:t="t2_destroy_target_01"
          target:t="t2_infantry_squad_01"
          team:t="Both"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t2_destroy_target_01"
          object:t="t2_infantry_squad_01"
          forceVisibleOnMap:b=yes
        }

        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.3
          target:t="enemy_waypoint_01"
          target:t="enemy_waypoint_02"
          team:t="Both"
        }

        varSetInt{
          value:i=0
          var:t="inf_number_to_kill_int_both"
          input_var:t="inf_number_to_kill_int_01"
        }

        varSetInt{
          value:i=0
          var:t="veh_number_to_kill_int_both"
          input_var:t="veh_number_to_kill_int"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="inf_number_to_kill_int_both"
          use_variable:b=yes
          var_value:t="inf_number_to_kill_int_02"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="veh_number_to_kill_int_both"
          use_variable:b=yes
          var_value:t="veh_number_to_kill_int_02"
        }

        triggerEnable{
          target:t="destroy_enemy_units_02"
          target:t="destroy_enemy_units_b"
          target:t="destroy_enemy_units_a"
        }
      }
    }

    destroy_enemy_units_a{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenCountMatches{
          object_type:t="isKilled"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          func:t="more"
          value:i=5
          object:t="t2_armored_units_squad_01"
          var:t="veh_number_to_kill_int"
        }

        infantryTroopWhenKilledByPlayerMatches{
          func:t="more"
          value:i=35
          object:t="t2_inf_squad_01"
          var:t="inf_number_to_kill_int_01"
        }
      }

      actions{
        playSound{
          name:t="sounds/gui/obj_complete"
          loop:b=no
          start:b=yes
        }

        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=1
          target:t="enemy_waypoint_01"
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    destroy_enemy_units_b{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenCountMatches{
          object_type:t="isKilled"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          func:t="more"
          value:i=5
          object:t="t2_armored_units_squad_02"
          var:t="veh_number_to_kill_int_02"
        }

        infantryTroopWhenKilledByPlayerMatches{
          func:t="more"
          value:i=15
          object:t="t2_inf_squad_02"
          var:t="inf_number_to_kill_int_02"
        }
      }

      actions{
        playSound{
          name:t="sounds/gui/obj_complete"
          loop:b=no
          start:b=yes
        }

        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=1
          target:t="enemy_waypoint_02"
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    destroy_enemy_units_02{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenCountMatches{
          object_type:t="isKilled"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          func:t="more"
          value:i=5
          object:t="t2_destroy_target_01"
          var:t="veh_number_to_kill_int_both"
        }

        infantryTroopWhenKilledByPlayerMatches{
          func:t="more"
          value:i=35
          object:t="t2_infantry_squad_01"
          var:t="inf_number_to_kill_int_both"
        }
      }

      actions{
        moSetObjectiveStatus{
          target:t="norway_helicopter_mission_attack_obj_03"
          status:i=2
        }

        triggerEnable{
          target:t="return_base_01"
          target:t="when_completed_objective"
        }

        unitWakeUp{
          target:t="gunboat_squad_01"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="gunboat_squad_01"
          targetAir:b=yes
          accuracy:r=0.28
          checkVisibilityTarget:b=yes
          effShootingRate:r=0.28
          airEffShootingRate:r=0.28
        }

        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=1
          target:t="enemy_waypoint_01"
          team:t="Both"
        }

        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=1
          target:t="enemy_waypoint_02"
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    complete_ab{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_01"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_02"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_03"
          status:t="completed"
        }

        gameWhenDifficulty{
          difficulty:t="arcade"
          is:t="equal"
        }
      }

      actions{
        missionCompleted{
          team:t="Both"
          showCompleteMessage:b=yes
          playCompleteMusic:b=yes
        }
      }

      else_actions{
      }
    }

    complete_rb{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_01"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_02"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_03"
          status:t="completed"
        }

        gameWhenDifficulty{
          difficulty:t="realistic"
          is:t="equal"
        }
      }

      actions{
        missionCompleted{
          team:t="Both"
          showCompleteMessage:b=yes
          playCompleteMusic:b=yes
        }
      }

      else_actions{
      }
    }

    exit_waypoint{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="exit_waypoint_01"
        }
      }

      actions{
        missionMarkAsWaypoint{
          visible:b=no
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=1
          target:t="exit_waypoint_01"
          team:t="Both"
        }

        moSetObjectiveStatus{
          target:t="norway_helicopter_mission_attack_obj_06"
          status:i=2
        }

        wait{
          time:r=3
        }

        missionCompleted{
          showCompleteMessage:b=yes
          playCompleteMusic:b=yes
        }
      }

      else_actions{
      }
    }

    return_base_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_01"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_02"
          status:t="completed"
        }

        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_03"
          status:t="completed"
        }

        gameWhenDifficulty{
          difficulty:t="simulator"
          is:t="equal"
        }
      }

      actions{
        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_04"
        }

        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=yes
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.5
          target:t="helipad_waypoint_01"
          team:t="Both"
        }

        triggerEnable{
          target:t="return_base_02"
        }
      }

      else_actions{
        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=yes
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.5
          target:t="exit_waypoint_01"
          team:t="Both"
        }

        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_06"
        }

        triggerEnable{
          target:t="exit_waypoint"
        }
      }
    }

    return_base_02{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="helipad_waypoint_01"
        }
      }

      actions{
        missionMarkAsWaypoint{
          visible:b=yes
          primary:b=no
          oriented:b=no
          ignoreDifficulty:b=yes
          scale:r=0.5
          target:t="helipad_waypoint_01"
          team:t="Both"
        }

        moSetObjectiveStatus{
          target:t="norway_helicopter_mission_attack_obj_04"
          status:i=2
        }

        wait{
          time:r=2
        }

        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_05"
        }

        triggerEnable{
          target:t="return_base_03"
        }
      }

      else_actions{
      }
    }

    return_base_03{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="t1_helipad_spawn_01"
          target:t="t1_helipad_spawn_02"
          target:t="t1_helipad_spawn_03"
        }

        unitWhenReachHeight{
          object_type:t="isAlive"
          object_marking:i=0
          check_objects:t="all"
          value:r=4
          comparasion_func:t="less"
          absolute_value:b=no
          object:t="t1_player01"
        }

        unitWhenControls{
          object:t="t1_player01"
          func:t="less"
          value:r=1
          property:t="power"
        }
      }

      actions{
        missionCompleted{
          team:t="Both"
          showCompleteMessage:b=yes
          playCompleteMusic:b=yes
        }
      }

      else_actions{
      }
    }

    secondary_objective_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="waypoint_01_07"
        }
      }

      actions{
        playHint{
          hintType:t="standard"
          name:t="Enemy units have been spotted near the town at P23-Q23. You can engage them but remember that it's not your primary objective"
          action:t="show"
          shouldFadeOut:b=no
          isOverFade:b=no
          time:r=12
          priority:i=1
          target_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
        }

        wait{
          time:r=13
        }

        moAddMissionObjective{
          target:t="norway_helicopter_mission_attack_obj_07"
        }

        triggerEnable{
          target:t="secondary_objective_complete_01"
        }
      }

      else_actions{
      }
    }

    secondary_objective_complete_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        infantryTroopWhenKilledByPlayerMatches{
          func:t="more"
          value:i=1
          object:t="t2_second_obj_inf_squad_01"
          var:t="inf_sec_number_to_kill_int_01"
        }

        unitWhenCountMatches{
          object_type:t="isKilled"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          func:t="more"
          value:i=1
          object:t="t2_second_obj_veh_squad_01"
          var:t="veh_sec_number_to_kill_int_01"
        }
      }

      actions{
        moSetObjectiveStatus{
          target:t="norway_helicopter_mission_attack_obj_07"
          status:i=2
          team:t="Both"
        }
      }

      else_actions{
      }
    }
  }

  mission_settings{
    isCategory:b=yes
    is_enabled:b=yes

    mission_settings_ab{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="arcade"
          is:t="equal"
        }
      }

      actions{
        missionAttempts{
          action:t="set"
          value:i=0
        }

        triggerEnable{
          target:t="set"
          target:t="when_hit"
          target:t="when_hit_hit"
        }
      }

      else_actions{
      }
    }

    mission_settings_rb{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="realistic"
          is:t="equal"
        }
      }

      actions{
        missionAttempts{
          action:t="set"
          value:i=0
        }

        triggerEnable{
          target:t="set"
          target:t="when_hit"
          target:t="when_hit_hit"
        }
      }

      else_actions{
      }
    }

    mission_settings_sb{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="simulator"
          is:t="equal"
        }
      }

      actions{
        missionAttempts{
          action:t="set"
          value:i=0
        }

        unitForceRearmSpeed{
          rearmSpeedK:r=0
          target:t="t1_player01"
        }

        triggerEnable{
          target:t="set"
          target:t="when_hit"
          target:t="when_hit_hit"
        }
      }

      else_actions{
      }
    }
  }

  debug_spotting{
    is_enabled:b=no
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=yes
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
    }

    actions{
      varSetString{
        value:t="alt_"
        var:t="debug_string"
      }

      varAddString{
        value:t=""
        digits:i=2
        var:t="debug_string"
        input_var:t="check_player_alt_var_int"
      }

      playHint{
        hintType:t="standard"
        name:t="@debug_string"
        action:t="show"
        shouldFadeOut:b=no
        isOverFade:b=no
        time:r=-1
        priority:i=0
        target_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
      }
    }

    else_actions{
    }
  }

  spawnzone_system{
    isCategory:b=yes
    is_enabled:b=yes

    when_in_area_01{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="waypoint_01_07"
        }
      }

      actions{
        varSetString{
          value:t=""
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_name_string"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="checkpoint_int_01"
        }

        varAddString{
          value:t=""
          digits:i=2
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_int_01"
        }
      }

      else_actions{
      }
    }

    when_in_area_02{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        unitWhenInArea{
          math:t="3D"
          object_type:t="isAlive"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          check_objects:t="any"
          object:t="t1_player01"
          target:t="waypoint_01_14"
        }
      }

      actions{
        varSetString{
          value:t=""
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_name_string"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="checkpoint_int_01"
        }

        varAddString{
          value:t=""
          digits:i=2
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_int_01"
        }
      }

      else_actions{
      }
    }

    when_completed_objective{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        misObjStatus{
          target:t="norway_helicopter_mission_attack_obj_03"
          status:t="completed"
        }
      }

      actions{
        varSetString{
          value:t=""
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_name_string"
        }

        varModify{
          operator:t="add"
          value:r=1
          var:t="checkpoint_int_01"
        }

        varAddString{
          value:t=""
          digits:i=2
          var:t="checkpoint_string_01"
          input_var:t="checkpoint_int_01"
        }
      }

      else_actions{
      }
    }

    respawn_ab{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="arcade"
          is:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }

        varCompareInt{
          var_value:t="respawn_ab"
          value:i=0
          comparasion_func:t="more"
        }
      }

      actions{
        missionSetFade{
          mode:t="fadeOut"
          color:p3=0, 0, 0
          time:r=2
        }

        wait{
          time:r=3
        }

        missionSetFade{
          mode:t="fadeIn"
          color:p3=0, 0, 0
          time:r=1
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t1_player01"
          speed:r=50
          lockSpeed:b=yes
        }

        unitSetControls{
          controls:t="power"
          value:r=0.5
          force:b=yes
          objects:t="t1_player01"
        }

        unitRespawn{
          delay:r=1
          offset:p3=0, 0, 0
          object:t="t1_player01"
          target:t="@checkpoint_string_01"
        }

        varModify{
          operator:t="add"
          value:r=-1
          var:t="respawn_ab"
        }

        varSetInt{
          value:i=5
          var:t="respawn_int"
          input_var:t="respawn_ab"
        }

        triggerEnable{
          target:t="respawn_waypoints_01"
          target:t="respawn_waypoints_02"
          target:t="hint_respawn_left"
        }
      }

      else_actions{
      }
    }

    respawn_rb{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="realistic"
          is:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }

        varCompareInt{
          var_value:t="respawn_rb"
          value:i=0
          comparasion_func:t="more"
        }
      }

      actions{
        missionSetFade{
          mode:t="fadeOut"
          color:p3=0, 0, 0
          time:r=2
        }

        wait{
          time:r=3
        }

        missionSetFade{
          mode:t="fadeIn"
          color:p3=0, 0, 0
          time:r=1
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t1_player01"
          speed:r=50
          lockSpeed:b=yes
        }

        unitSetControls{
          controls:t="power"
          value:r=0.5
          force:b=yes
          objects:t="t1_player01"
        }

        unitRespawn{
          delay:r=1
          offset:p3=0, 0, 0
          object:t="t1_player01"
          target:t="@checkpoint_string_01"
        }

        varModify{
          operator:t="add"
          value:r=-1
          var:t="respawn_rb"
        }

        varSetInt{
          value:i=2
          var:t="respawn_int"
          input_var:t="respawn_rb"
        }

        triggerEnable{
          target:t="respawn_waypoints_01"
          target:t="respawn_waypoints_02"
          target:t="hint_respawn_left"
        }
      }

      else_actions{
      }
    }

    respawn_cus{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=yes
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="custom"
          is:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }

        varCompareInt{
          var_value:t="respawn_ab"
          value:i=0
          comparasion_func:t="more"
        }
      }

      actions{
        missionSetFade{
          mode:t="fadeOut"
          color:p3=0, 0, 0
          time:r=2
        }

        wait{
          time:r=3
        }

        missionSetFade{
          mode:t="fadeIn"
          color:p3=0, 0, 0
          time:r=1
        }

        unitRespawn{
          delay:r=1
          offset:p3=0, 0, 0
          object:t="t1_player01"
          target:t="@checkpoint_string_01"
        }

        unitSetProperties{
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          object:t="t1_player01"
          speed:r=50
          lockSpeed:b=yes
        }

        unitSetControls{
          controls:t="power"
          value:r=0.5
          force:b=yes
          objects:t="t1_player01"
        }

        varModify{
          operator:t="add"
          value:r=-1
          var:t="respawn_ab"
        }

        varSetInt{
          value:i=5
          var:t="respawn_int"
          input_var:t="respawn_ab"
        }

        triggerEnable{
          target:t="respawn_waypoints_01"
          target:t="respawn_waypoints_02"
          target:t="hint_respawn_left"
        }
      }

      else_actions{
      }
    }

    respawn_waypoints_01{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        varCompareString{
          var_value:t="checkpoint_string_01"
          value:t="checkpoint_00"
          comparasion_func:t="equal"
        }
      }

      actions{
        triggerEnable{
          target:t="takeoff_waypoint"
        }
      }

      else_actions{
      }
    }

    respawn_waypoints_02{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        varCompareString{
          var_value:t="checkpoint_string_01"
          value:t="checkpoint_01"
          comparasion_func:t="equal"
        }
      }

      actions{
        triggerEnable{
          target:t="takeoff_waypoint_no_obj"
        }
      }

      else_actions{
      }
    }

    hint_respawn_left{
      is_enabled:b=no
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
      }

      actions{
        varSetString{
          value:t=""
          var:t="respawn_string_01"
          input_var:t="respawn_string_name"
        }

        varAddString{
          value:t=""
          digits:i=1
          var:t="respawn_string_01"
          input_var:t="respawn_int"
        }

        playHint{
          hintType:t="standard"
          name:t="@respawn_string_01"
          action:t="show"
          shouldFadeOut:b=no
          isOverFade:b=no
          time:r=4
          priority:i=0
          target_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
        }
      }

      else_actions{
      }
    }
  }

  fission_mailed{
    isCategory:b=yes
    is_enabled:b=yes

    ab_fail{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        varCompareInt{
          var_value:t="respawn_ab"
          value:i=0
          comparasion_func:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }
      }

      actions{
        wait{
          time:r=2
        }

        missionFailed{
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    sb_fail{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        gameWhenDifficulty{
          difficulty:t="simulator"
          is:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }
      }

      actions{
        wait{
          time:r=3
        }

        missionFailed{
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    rb_fail{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        varCompareInt{
          var_value:t="respawn_rb"
          value:i=0
          comparasion_func:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }
      }

      actions{
        wait{
          time:r=2
        }

        missionFailed{
          team:t="Both"
        }
      }

      else_actions{
      }
    }

    cus_fail{
      is_enabled:b=yes
      comments:t=""

      props{
        actionsType:t="PERFORM_ONE_BY_ONE"
        conditionsType:t="ALL"
        enableAfterComplete:b=no
      }

      events{
        periodicEvent{
          time:r=1
        }
      }

      conditions{
        varCompareInt{
          var_value:t="respawn_ab"
          value:i=0
          comparasion_func:t="equal"
        }

        unitWhenStatus{
          object_type:t="isKilled"
          check_objects:t="any"
          object_marking:i=0
          object_var_name:t=""
          object_var_comp_op:t="equal"
          object_var_value:i=0
          target_type:t="isAlive"
          check_period:r=1
          object:t="t1_player01"
        }
      }

      actions{
        wait{
          time:r=2
        }

        missionFailed{
          team:t="Both"
        }
      }

      else_actions{
      }
    }
  }
}

mission_objectives{
  isCategory:b=yes
  is_enabled:b=yes

  norway_helicopter_mission_attack_obj_01{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_02{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_03{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_04{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_05{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_06{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=yes
      timeLimit:i=1800
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }

  norway_helicopter_mission_attack_obj_07{
    is_enabled:b=no
    comments:t=""
    type:t="abstractMissionObjective"

    props{
      isPrimary:b=no
      timeLimit:i=1800
      failDesc:t=""
      team:t="Both"
    }

    onSuccess{
    }

    onFailed{
    }
  }
}

variables{
  check_player_alt_var_int:i=0
  first_waypoint_string_01:t=""
  first_waypoint_int_01:i=1
  second_waypoint_string_01:t=""
  second_waypoint_int_01:i=2
  waypoint_name_var:t=""
  last_waypoint_trigger_string_01:t="destroy_enemy_units_01"
  inf_number_to_kill_int_01:i=15
  inf_number_to_kill_int_02:i=0
  inf_number_to_kill_int_both:i=0
  veh_number_to_kill_int:i=10
  veh_number_to_kill_int_02:i=0
  veh_number_to_kill_int_both:i=0
  inf_sec_number_to_kill_int_01:i=0
  veh_sec_number_to_kill_int_01:i=0
  loop_bot_settings:i=0
  debug_string:t=""
  random_var_destroyed_vehicles:i=0
  random_var_killed_inf:i=0
  checkpoint_string_01:t="checkpoint_00"
  checkpoint_int_01:i=0
  checkpoint_name_string:t="checkpoint_"
  respawn_ab:i=5
  respawn_rb:i=2
  respawn_string_01:t=""
  respawn_string_name:t="Respawns left: "
  respawn_int:i=0
  checkpoint_00:t="waypoint_01_01"
  checkpoint_01:t="waypoint_01_08"
}

dialogs{
}

airfields{
}

effects{
}

units{
  objectGroups{
    name:t="t1_helipad01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25281.1, 97.2261, 4636.03]]
    unit_class:t="dynhelipad_beton_a_usa"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  objectGroups{
    name:t="t1_camp01"
    tm:m=[[-0.741223, 0, -0.671258] [0, 1, 0] [0.671258, 0, -0.741223] [25576.2, 96.4853, 4472.6]]
    unit_class:t="alliance_big_camp_pit_entrenchment_s"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  objectGroups{
    name:t="t1_camp02"
    tm:m=[[-0.997341, 0, 0.072877] [0, 1, 0] [-0.072877, 0, -0.997341] [25075.6, 99.7293, 4386.68]]
    unit_class:t="alliance_big_camp_pit_entrenchment_s"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  objectGroups{
    name:t="t1_camp03"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [24814.9, 100.066, 4512.76]]
    unit_class:t="trench"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  objectGroups{
    name:t="objectGroups_03"
    tm:m=[[0.0994091, 0, -0.995047] [0, 1, 0] [0.995047, 0, 0.0994091] [25263.5, 100.066, 4268.93]]
    unit_class:t="trench"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  objectGroups{
    name:t="t1_camp04"
    tm:m=[[0.730469, 0, -0.682946] [0, 1, 0] [0.682946, 0, 0.730469] [25872.6, 100.066, 4609.81]]
    unit_class:t="trench"
    objLayer:i=2

    props{
      army:i=1
      active:b=yes
    }
  }

  armada{
    name:t="t1_player01"
    tm:m=[[-1, 0, 2.08616e-07] [0, 1, 0] [-2.08616e-07, 0, -1] [25301.3, 99.3154, 4731]]
    unit_class:t="ah_1g"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t="ah_1g_rocket"
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      free_distance:r=70
      floating_distance:r=50
      minimum_distance_to_earth:r=20
      altLimit:r=6000
      attack_type:t="fire_at_will"
      skill:i=4
      speed:r=0

      plane{
        wing_formation:t="Diamond"
        row_distances:r=3
        col_distances:r=3
        super_formation:t="Diamond"
        super_row_distances:r=1.5
        super_col_distances:r=1.5
        ai_skill:t="NORMAL"
        task:t="FLY_WAYPOINT"
      }
    }

    way{
    }
  }

  armada{
    name:t="t1_heli_bot01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [39679.8, 1937.07, 2521.32]]
    unit_class:t="ah_1g"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t="ah_1g_rocket_ffar"
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      free_distance:r=70
      floating_distance:r=50
      minimum_distance_to_earth:r=20
      altLimit:r=200
      attack_type:t="fire_at_will"
      skill:i=4

      plane{
        wing_formation:t="Diamond"
        row_distances:r=3
        col_distances:r=3
        super_formation:t="Diamond"
        super_row_distances:r=1.5
        super_col_distances:r=1.5
        ai_skill:t="NORMAL"
        task:t="FLY_WAYPOINT"
      }
    }

    way{
    }
  }

  squad{
    name:t="t1_heli_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25246.3, 93.2046, 4696.9]]

    props{
      squad_members:t="t1_player01"
      squad_members:t="t1_heli_bot01"
    }
  }

  tankModels{
    name:t="t2_spaa01"
    tm:m=[[0.461749, 0, -0.887011] [0, 1, 0] [0.887011, 0, 0.461749] [20622.4, 161.316, 4445.56]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  squad{
    name:t="aaa_effi_squad"
    tm:m=[[0.461749, 0, -0.887011] [0, 1, 0] [0.887011, 0, 0.461749] [20081.5, 187.1, 4307.08]]

    props{
      squad_members:t="t2_spaa01"
      squad_members:t="t2_spaa_03"
      squad_members:t="t2_spaa_01"
      squad_members:t="t2_spaa_02"
      squad_members:t="t2_tank_01"
      squad_members:t="t2_tank_02"
      squad_members:t="t2_tank_03"
      squad_members:t="t2_tank_04"
      squad_members:t="t2_inf_veh_01"
      squad_members:t="t2_inf_veh_02"
      squad_members:t="t2_inf_veh_03"
      squad_members:t="t2_inf_veh_04"
      squad_members:t="t2_inf_veh_05"
      squad_members:t="t2_inf_veh_06"
      squad_members:t="t2_inf_veh_07"
      squad_members:t="t2_inf_veh_08"
      squad_members:t="t2_tank_05"
      squad_members:t="t2_inf_veh_09"
      squad_members:t="t2_inf_veh_11"
      squad_members:t="t2_inf_veh_10"
      squad_members:t="t2_spaa02"
      squad_members:t="t2_spaa03"
      squad_members:t="t2_spaa04"
      squad_members:t="t2_spaa05"
      squad_members:t="t2_spaa06"
      squad_members:t="t2_inf_veh_12"
      squad_members:t="t2_boat_01"
      squad_members:t="t2_boat_02"
      squad_members:t="t2_tank_06"
      squad_members:t="t2_inf_veh_13"
      squad_members:t="t2_spaa08"
      squad_members:t="t2_spaa09"
      squad_members:t="t2_spaa07"
      squad_members:t="t2_spaa10"
      squad_members:t="t2_spaa11"
      squad_members:t="t2_boat_03"
      squad_members:t="t2_spaa13"
      squad_members:t="t2_spaa14"
      squad_members:t="t2_inf_stationy_20"
      squad_members:t="t2_spaa12"
      squad_members:t="t2_sec_veh_01"
      squad_members:t="t2_sec_veh_04"
      squad_members:t="t2_sec_veh_03"
      squad_members:t="t2_sec_veh_02"
    }
  }

  structures{
    name:t="cutscene_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [23951.1, 153.042, 3678.62]]
    unit_class:t="dummy"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  structures{
    name:t="cutscene_01"
    tm:m=[[-0.000812776, 0, -0.000582577] [0, 0.001, 0] [0.000582577, 0, -0.000812776] [26560.9, 392.775, 5641.73]]
    unit_class:t="dummy_immortal"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  squad{
    name:t="all_enemy_units_squad"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25780.5, 290.447, 6638.71]]

    props{
      squad_members:t="t2_spaa01"
      squad_members:t="t2_spaa_01"
      squad_members:t="t2_spaa_02"
      squad_members:t="t2_tank_01"
      squad_members:t="t2_tank_02"
      squad_members:t="t2_tank_03"
      squad_members:t="t2_tank_04"
      squad_members:t="t2_inf_veh_01"
      squad_members:t="t2_inf_veh_02"
      squad_members:t="t2_inf_veh_03"
      squad_members:t="t2_inf_veh_04"
      squad_members:t="t2_inf_veh_05"
      squad_members:t="t2_inf_veh_06"
      squad_members:t="t2_inf_veh_07"
      squad_members:t="t2_inf_veh_08"
      squad_members:t="t2_tank_05"
      squad_members:t="t2_inf_veh_09"
      squad_members:t="t2_inf_veh_11"
      squad_members:t="t2_spaa_03"
      squad_members:t="t2_inf_veh_10"
      squad_members:t="t2_spaa02"
      squad_members:t="t2_spaa03"
      squad_members:t="t2_spaa04"
      squad_members:t="t2_spaa05"
      squad_members:t="t2_spaa06"
      squad_members:t="t2_inf_veh_12"
      squad_members:t="t2_boat_01"
      squad_members:t="t2_boat_02"
      squad_members:t="t2_tank_06"
      squad_members:t="t2_inf_veh_13"
      squad_members:t="t2_spaa08"
      squad_members:t="t2_spaa09"
      squad_members:t="t2_spaa10"
      squad_members:t="t2_spaa07"
      squad_members:t="t2_spaa11"
      squad_members:t="t2_boat_03"
      squad_members:t="t2_spaa13"
      squad_members:t="t2_spaa14"
      squad_members:t="t2_inf_stationy_20"
      squad_members:t="t2_spaa12"
      squad_members:t="t2_sec_veh_01"
      squad_members:t="t2_sec_veh_04"
      squad_members:t="t2_sec_veh_03"
      squad_members:t="t2_sec_veh_02"
    }
  }

  squad{
    name:t="t1_squad"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [26066.1, 336.58, 6642.61]]

    props{
      squad_members:t="t1_player01"
    }
  }

  wheeled_vehicles{
    name:t="t1_stationary_vehicles_01"
    tm:m=[[0.735443, 0, -0.677587] [0, 1, 0] [0.677587, 0, 0.735443] [25466.2, 102.375, 4408.99]]
    unit_class:t="us_dodge_wc51"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  wheeled_vehicles{
    name:t="t1_stationary_vehicles_02"
    tm:m=[[0.735443, 0, -0.677587] [0, 1, 0] [0.677587, 0, 0.735443] [25459.5, 102.375, 4415.12]]
    unit_class:t="us_dodge_wc51"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_03"
    tm:m=[[0.774653, 0, 0.632387] [0, 1, 0] [-0.632387, 0, 0.774653] [25647.3, 102.427, 4489.87]]
    unit_class:t="us_truck_us6_studebaker_board"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_04"
    tm:m=[[0.297906, 0, 0.954595] [0, 1, 0] [-0.954595, 0, 0.297906] [25675.9, 102.427, 4513.24]]
    unit_class:t="us_truck_us6_studebaker_board"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_05"
    tm:m=[[0.607621, 0, -0.794227] [0, 1, 0] [0.794227, 0, 0.607621] [25606.9, 102.427, 4467.1]]
    unit_class:t="us_m60a1_rise_passive_era"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_06"
    tm:m=[[0.99814, 0, -0.060968] [0, 1, 0] [0.060968, 0, 0.99814] [25336.6, 98.3829, 4577.82]]
    unit_class:t="us_m60a1_rise_passive_era"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_07"
    tm:m=[[0.608042, 0, -0.793905] [0, 1, 0] [0.793905, 0, 0.608042] [25348.3, 98.3829, 4551.25]]
    unit_class:t="us_m60a1_rise_passive_era"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t1_stationary_vehicles_08"
    tm:m=[[0.132068, 0, -0.991241] [0, 1, 0] [0.991241, 0, 0.132068] [25175.8, 100.326, 4419.13]]
    unit_class:t="us_m60a1_rise_passive_era"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25343.9, 98.3443, 4578.04]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25343.9, 98.3443, 4562.24]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_03"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25257.2, 98.3443, 4595.04]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_04"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25228.1, 98.3443, 4595.04]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_05"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25318.8, 98.3443, 4590.73]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=yes
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=1
    }

    way{
      t1_stationary_infantry_05_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25295.9, 95.3816, 4591.42]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25267, 95.1422, 4591.95]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25254.4, 95.1623, 4586.98]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25234.7, 95.2086, 4586.88]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25239.8, 96.682, 4570.25]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25250.6, 97.7215, 4556.03]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_07{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25274.7, 96.1552, 4563.44]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_08{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25281.5, 97.1872, 4550.68]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_09{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25286, 97.0496, 4550.49]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_10{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25288.3, 96.5455, 4554.79]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_11{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25302.2, 96.0524, 4565.5]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_12{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25315.7, 96.0618, 4569.53]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_13{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25316.3, 95.7212, 4583.93]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_05_wp_14{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25316.6, 95.5177, 4592.53]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t1_stationary_infantry_06"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25380.4, 98.3443, 4574.75]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_07"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25380.4, 102.47, 4436.59]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_08"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25432, 100.924, 4460.71]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_09"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25470.9, 101.489, 4441.51]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=1
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_10"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25470.9, 98.555, 4516.35]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_11"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25541.2, 98.8186, 4528.39]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_12"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25515.8, 97.0784, 4592.66]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=4
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_13"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25573.4, 98.8686, 4569.63]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_14"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25614.7, 101.264, 4509.39]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_15"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25517.4, 100.834, 4436.51]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_16"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25298, 101.805, 4436.51]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_17"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25298, 100.554, 4358.89]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=4
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_18"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25211.7, 99.5561, 4381.92]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_19"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25113.2, 100.218, 4433.01]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_20"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25038.7, 99.9031, 4443.01]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=1
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_21"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25113.2, 101.613, 4482.01]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_22"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25610, 99.6308, 4602.14]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t1_stationary_infantry_23"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25171.5, 102.082, 4482.01]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=yes
    isShipSpline:b=yes
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=1
    }

    way{
      t1_stationary_infantry_23_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25246.1, 102.66, 4481.23]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25349.4, 102.667, 4452.25]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25385.5, 101.087, 4386.54]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25323.8, 100.853, 4374.29]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25189.2, 99.1049, 4362.68]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25152.3, 99.74, 4405.17]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_23_wp_07{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25167, 101.137, 4450.08]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t1_stationary_infantry_24"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25405.8, 101.805, 4436.51]]
    unit_class:t="cu_usa_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=yes
    isShipSpline:b=yes
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      attack_type:t="fire_at_will"
      count:i=1
    }

    way{
      t1_stationary_infantry_24_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25448.5, 101.124, 4452.99]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25483.6, 99.6349, 4475.47]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25511.2, 98.8568, 4516.95]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25536.6, 98.3907, 4544.72]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25535.9, 97.1461, 4596.4]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25507, 96.8809, 4598.02]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_07{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25472.8, 97.6483, 4554.78]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_08{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25449.1, 98.8429, 4497.2]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t1_stationary_infantry_24_wp_09{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25424, 100.102, 4471.77]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_spaa_01"
    tm:m=[[0.300706, 0, -0.953717] [0, 1, 0] [0.953717, 0, 0.300706] [2551.01, 12.6598, -4836.73]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa_02"
    tm:m=[[0.300706, 0, -0.953717] [0, 1, 0] [0.953717, 0, 0.300706] [2892.23, 11.5233, -6093.38]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_tank_01"
    tm:m=[[0.672736, 0, 0.739883] [0, 1, 0] [-0.739883, 0, 0.672736] [2768.99, 12.434, -4492.08]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_tank_01_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2764.12, 12.4312, -4457.68]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_01_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2738.2, 12.4452, -4405.01]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_01_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2722.23, 12.7823, -4303.53]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_01_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2741.24, 12.3393, -4233.87]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_tank_02"
    tm:m=[[0.724171, 0, 0.689621] [0, 1, 0] [-0.689621, 0, 0.724171] [2756.89, 12.434, -4502.86]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_tank_03"
    tm:m=[[0.698231, 0, 0.715872] [0, 1, 0] [-0.715872, 0, 0.698231] [2744.12, 12.434, -4512.98]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_tank_03_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2755.55, 12.4524, -4514.71]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_03_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2798.06, 12.4061, -4496.16]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_03_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2910.92, 12.3867, -4472.76]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_03_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [3068.7, 14.0769, -4404.8]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_tank_04"
    tm:m=[[0.698231, 0, 0.715872] [0, 1, 0] [-0.715872, 0, 0.698231] [2730.3, 12.434, -4527.15]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2758.4, 12.4447, -4492.72]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
      t2_inf_01_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2788.11, 12.417, -4500.51]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_01_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2837.96, 12.3649, -4488.38]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_01_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2981.13, 12.3237, -4520.28]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2742.26, 12.4447, -4501.35]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
      t2_inf_02_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2724.37, 12.4721, -4464.64]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_02_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2728.68, 12.4631, -4443.3]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_03"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2725.36, 12.4447, -4521.74]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
      t2_inf_03_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2700.84, 12.5089, -4525.03]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_03_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2669.2, 12.5411, -4529.04]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_01"
    tm:m=[[0.699259, 0, 0.714869] [0, 1, 0] [-0.714869, 0, 0.699259] [2715.24, 12.4981, -4540.62]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_01_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2744.89, 12.4681, -4537.69]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_01_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2834.92, 12.378, -4533.85]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_01_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2944.14, 12.2835, -4595.14]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_02"
    tm:m=[[0.699259, 0, 0.714869] [0, 1, 0] [-0.714869, 0, 0.699259] [2801.03, 13.0558, -4293.71]]
    unit_class:t="ussr_bmp_2"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_02_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2807.71, 12.6287, -4260.13]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_02_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2795.77, 12.2628, -4222.12]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_02_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2803.6, 12.2255, -4202.12]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_02_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2800.15, 12.157, -4183.22]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_04"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2798.39, 13.0818, -4287.58]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_03"
    tm:m=[[0.937292, 0, -0.348546] [0, 1, 0] [0.348546, 0, 0.937292] [2692.52, 12.4981, -4712.77]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_03_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2696.46, 12.5572, -4722.46]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_03_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2698.25, 12.5576, -4732.63]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_03_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2694.49, 12.9806, -4748.82]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_03_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2706.12, 12.9675, -4804.14]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_03_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2713.85, 12.9906, -4822.77]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_04"
    tm:m=[[0.937292, 0, -0.348546] [0, 1, 0] [0.348546, 0, 0.937292] [2678.95, 12.4981, -4707.73]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_05"
    tm:m=[[0.970666, 0, -0.24043] [0, 1, 0] [0.24043, 0, 0.970666] [2709.14, 12.4981, -4715.49]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_05_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2731.61, 12.9789, -4732.92]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_05_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2762.16, 13.6653, -4741.78]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_05_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2768.88, 13.8336, -4762.93]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_05_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2798.03, 13.4052, -4830.76]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_06"
    tm:m=[[0.642754, 0, -0.766073] [0, 1, 0] [0.766073, 0, 0.642754] [2481.93, 12.4981, -4849.22]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_06_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2466.18, 12.6761, -4860.24]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_06_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2454.28, 12.6792, -4869.34]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_06_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2454.84, 12.6814, -4888]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_07"
    tm:m=[[0.855998, 0, -0.51698] [0, 1, 0] [0.51698, 0, 0.855998] [2464.4, 12.4981, -4845.04]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_08"
    tm:m=[[0.725181, 0, -0.688558] [0, 1, 0] [0.688558, 0, 0.725181] [2495.04, 12.4981, -4859.8]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_08_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2497.25, 12.6758, -4893.46]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_08_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2466.6, 12.6855, -4929.06]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_08_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2440.74, 12.6878, -4918.44]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_05"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2720.59, 12.5295, -4705.43]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
      t2_inf_05_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2673.25, 12.5702, -4677.71]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_05_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2599.73, 12.6359, -4645.47]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_05_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2544.7, 12.6494, -4619.17]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_06"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2690.55, 12.5295, -4694.09]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
      t2_inf_06_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2669.03, 12.5783, -4695.03]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_06_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2652.23, 12.5988, -4712.67]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_06_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2625.02, 12.6402, -4776.67]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_06_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2625.65, 12.6483, -4834.72]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_06_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2632.14, 12.6486, -4843.6]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_06_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2646.7, 12.6983, -4840.56]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_07"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2489.25, 12.5295, -4847.13]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
      t2_inf_07_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2486.95, 12.6747, -4874.25]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_07_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2479.2, 12.6766, -4879.93]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_08"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2474.51, 12.6724, -4840.61]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
      t2_inf_08_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2465.54, 12.6728, -4831.88]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_08_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2448.17, 12.6759, -4834.17]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_08_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2437.21, 12.6789, -4843.97]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_tank_05"
    tm:m=[[0.996665, 0, -0.0816029] [0, 1, 0] [0.0816029, 0, 0.996665] [4246.71, 12.8572, -1684.92]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_tank_05_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4316.89, 11.0928, -1657.18]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_05_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4373.54, 12.186, -1610.19]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_05_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4396.73, 12.7477, -1585.28]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_09"
    tm:m=[[0.999947, 0, -0.0103287] [0, 1, 0] [0.0103287, 0, 0.999947] [4233.74, 15.2173, -1780.57]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_09_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4265.94, 15.2937, -1807.26]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_09_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4316.14, 15.1223, -1835.95]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_inf_veh_11"
    tm:m=[[1, 0, 0.000341803] [0, 1, 0] [-0.000341803, 0, 1] [3937.64, 11.9216, -1600.14]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_09"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4236.12, 13.044, -1685.57]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_10"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [4209.54, 15.117, -1754.92]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=5
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_11"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3938.06, 11.9661, -1592.82]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_12"
    tm:m=[[0.979212, 0, 0.202837] [0, 1, 0] [-0.202837, 0, 0.979212] [2479.31, 12.661, -4403.82]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_12"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2485.28, 12.6612, -4389.8]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
      t2_inf_12_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2471.98, 12.664, -4331.88]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_14"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2524.65, 12.6724, -4972.35]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=6
      distributionRadius:r=40
    }

    way{
      t2_inf_14_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2505.81, 12.6838, -4959.03]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_14_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2468.2, 12.6904, -4965.48]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_15"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2433.15, 12.6724, -4672.89]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=40
    }

    way{
      t2_inf_15_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2452.93, 12.655, -4625.09]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_15_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2476.59, 12.6553, -4572.62]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_16"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2790.48, 12.6724, -4672.89]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=7
      distributionRadius:r=40
    }

    way{
      t2_inf_16_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2765.01, 13.5776, -4737.77]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_16_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2750.46, 13.1423, -4828.43]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_17"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2705.83, 12.5426, -4235.61]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=40
    }

    way{
      t2_inf_17_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2692.55, 12.1023, -4213.52]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_spaa_03"
    tm:m=[[0.300706, 0, -0.953717] [0, 1, 0] [0.953717, 0, 0.300706] [7425.17, 30.3595, -3624.28]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_18"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [7405.24, 30.7257, -3609.9]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_10"
    tm:m=[[0.529891, 0, 0.848066] [0, 1, 0] [-0.848066, 0, 0.529891] [7408.63, 30.8902, -3636.18]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_19"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [7430.83, 30.7257, -3634.78]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  area_squad{
    name:t="all_spot_area_squad"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [1872.16, 0, -2568.97]]

    props{
      squad_members:t="all_spot_area_01"
      squad_members:t="all_spot_area_02"
      squad_members:t="all_spot_area_03"
      squad_members:t="all_spot_area_04"
      squad_members:t="all_spot_area_05"
      squad_members:t="all_spot_area_06"
      squad_members:t="all_spot_area_07"
      squad_members:t="all_spot_area_08"
    }
  }

  squad{
    name:t="t2_destroy_target_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [6893.55, 204.438, -1850.26]]

    props{
      squad_members:t="t2_tank_01"
      squad_members:t="t2_tank_02"
      squad_members:t="t2_tank_03"
      squad_members:t="t2_tank_04"
      squad_members:t="t2_inf_veh_01"
      squad_members:t="t2_inf_veh_02"
      squad_members:t="t2_inf_veh_03"
      squad_members:t="t2_inf_veh_04"
      squad_members:t="t2_inf_veh_05"
      squad_members:t="t2_inf_veh_06"
      squad_members:t="t2_inf_veh_07"
      squad_members:t="t2_inf_veh_08"
      squad_members:t="t2_tank_05"
      squad_members:t="t2_inf_veh_09"
      squad_members:t="t2_inf_veh_11"
      squad_members:t="t2_inf_veh_10"
      squad_members:t="t2_tank_06"
      squad_members:t="t2_inf_veh_13"
      squad_members:t="t2_spaa_01"
    }
  }

  squad{
    name:t="t2_infantry_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [7029.33, 131.073, -1674.73]]

    props{
      squad_members:t="t2_inf_01"
      squad_members:t="t2_inf_02"
      squad_members:t="t2_inf_03"
      squad_members:t="t2_inf_04"
      squad_members:t="t2_inf_05"
      squad_members:t="t2_inf_06"
      squad_members:t="t2_inf_07"
      squad_members:t="t2_inf_08"
      squad_members:t="t2_inf_09"
      squad_members:t="t2_inf_10"
      squad_members:t="t2_inf_11"
      squad_members:t="t2_inf_12"
      squad_members:t="t2_inf_14"
      squad_members:t="t2_inf_15"
      squad_members:t="t2_inf_16"
      squad_members:t="t2_inf_17"
      squad_members:t="t2_inf_19"
      squad_members:t="t2_inf_13"
      squad_members:t="t2_inf_20"
      squad_members:t="t2_inf_21"
      squad_members:t="t2_inf_22"
      squad_members:t="t2_inf_23"
      squad_members:t="t2_inf_24"
      squad_members:t="t2_inf_25"
      squad_members:t="t2_inf_26"
      squad_members:t="t2_inf_27"
      squad_members:t="t2_inf_28"
      squad_members:t="t2_inf_29"
      squad_members:t="t2_inf_30"
      squad_members:t="t2_inf_31"
      squad_members:t="t2_inf_32"
      squad_members:t="t2_inf_33"
      squad_members:t="t2_inf_34"
      squad_members:t="t2_inf_35"
      squad_members:t="t2_inf_36"
      squad_members:t="t2_inf_37"
      squad_members:t="t2_inf_38"
      squad_members:t="t2_inf_39"
      squad_members:t="t2_inf_40"
      squad_members:t="t2_inf_41"
      squad_members:t="t2_inf_42"
      squad_members:t="t2_inf_43"
      squad_members:t="t2_inf_44"
      squad_members:t="t2_inf_45"
      squad_members:t="t2_inf_46"
      squad_members:t="t2_inf_47"
      squad_members:t="t2_inf_48"
    }
  }

  structures{
    name:t="cutscene_03"
    tm:m=[[-0.604335, 0, -0.79673] [0, 1, 0] [0.79673, 0, -0.604335] [25367.7, 700, 4577.64]]
    unit_class:t="dummy_immortal"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  structures{
    name:t="cutscene_04"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25277.8, 93.9459, 4645.4]]
    unit_class:t="dummy_immortal"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  structures{
    name:t="cutscene_05"
    tm:m=[[-0.865135, 0, -0.501539] [0, 1, 0] [0.501539, 0, -0.865135] [25303.4, 98.3, 4731.96]]
    unit_class:t="dummy_immortal"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  structures{
    name:t="cutscene_06"
    tm:m=[[-0.866025, 0, -0.5] [0, 1, 0] [0.5, 0, -0.866025] [25087.4, 102.7, 4583.59]]
    unit_class:t="dummy_immortal"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa02"
    tm:m=[[0.461749, 0, -0.887011] [0, 1, 0] [0.887011, 0, 0.461749] [19707.8, 120.981, 3526.13]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa03"
    tm:m=[[0.461749, 0, -0.887011] [0, 1, 0] [0.887011, 0, 0.461749] [18682.7, 78.0595, 2734.44]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa04"
    tm:m=[[0.932048, 0, -0.362335] [0, 1, 0] [0.362335, 0, 0.932048] [15781.6, 56.4208, 1680.5]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa05"
    tm:m=[[0.924628, 0, 0.380872] [0, 1, 0] [-0.380872, 0, 0.924628] [12921.8, 19.7042, 1111.58]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa06"
    tm:m=[[0.924628, 0, 0.380872] [0, 1, 0] [-0.380872, 0, 0.924628] [10432.1, 26.4014, -1264.46]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_01"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13187.4, 11.0313, 777.262]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_01_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13167.4, 10.7254, 767.238]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_01_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13155.9, 10.5177, 751.96]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_01_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13151.1, 10.411, 734.91]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_02"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13187.4, 11.7593, 389.941]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=5
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_03"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13187.4, 13.1164, -341.543]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_03_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13250.8, 21.5978, -350.077]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_03_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13287.7, 26.7761, -364.413]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_03_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13305.7, 29.0029, -371.294]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_04"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13324.4, 33.9969, -341.543]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_05"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13501.6, 51.3245, -341.543]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_06"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13501.6, 44.5876, -462.03]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_06_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13502.4, 46.3299, -431.471]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_06_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13489.9, 46.6805, -416.182]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_07"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13209.9, 9.41096, -423.134]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_07_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13243.9, 14.2086, -445.78]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_07_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13270.2, 17.601, -453.769]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_08"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [12708.5, 14.4983, -704.641]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_08_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [12600, 0, -700]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_09"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [12643.3, 14.354, -757.281]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_10"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [12411.2, 12.12, -757.281]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa07"
    tm:m=[[0.954032, 0, -0.299705] [0, 1, 0] [0.299705, 0, 0.954032] [10437.1, 24.3853, -1243.66]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_11"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [10420.8, 24.714, -1253.58]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_12"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13428.6, 33.9969, -349.874]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_13"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13396.6, 26.819, -516.428]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_13_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13431.1, 35.978, -500.987]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_14"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13272.3, 12.366, 500.44]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_14_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13252.4, 12.19, 497.293]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_14_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13231.7, 11.9007, 501.913]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_15"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13241.7, 11.5667, 607.233]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_16"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13266.8, 12.1335, 708.928]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_16_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13271, 12.1556, 676.146]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_16_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13264.4, 12.027, 663.203]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_16_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13253.2, 11.8374, 654.622]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_17"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13034.6, 10.349, 456.413]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
      t2_inf_stationy_17_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13062.2, 10.4672, 470.171]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_stationy_17_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13058.2, 10.1902, 487.482]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_stationy_18"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [13131.3, 9.94348, 652.498]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  ships{
    name:t="t2_boat_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [12093.2, 0, -125.044]]
    unit_class:t="ussr_pr_123k"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  ships{
    name:t="t2_boat_02"
    tm:m=[[0.835097, 0, 0.550102] [0, 1, 0] [-0.550102, 0, 0.835097] [12600, 0, 400]]
    unit_class:t="ussr_pr_1204_late"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_inf_veh_13"
    tm:m=[[0.963968, 0, -0.266017] [0, 1, 0] [0.266017, 0, 0.963968] [3957.76, 11.9216, -1613.19]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_inf_veh_13_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [3981.57, 11.2999, -1655.25]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_13_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4006.08, 10.9652, -1735.19]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_veh_13_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4005.63, 11.3084, -1768.62]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_13"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3958.67, 11.5985, -1630.5]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_20"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [4058.04, 16.4905, -1555.44]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_21"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3989.6, 16.4015, -1516.55]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_22"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [4005.63, 16.4015, -1532.97]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_23"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [4093.12, 16.4015, -1447.57]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_24"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3999.56, 16.4015, -1420.83]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_25"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3896.63, 16.4015, -1373.89]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=5
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_26"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3808.46, 38.0847, -1459.94]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_27"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3914.63, 24.3158, -1249.24]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_28"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [4173.01, 15.117, -1664.74]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=5
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_29"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [4172.82, 15.117, -1682.29]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=5
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_30"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [4164.33, 15.117, -1721.3]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_31"
    tm:m=[[0.698476, 0, -0.715634] [0, 1, 0] [0.715634, 0, 0.698476] [3763.29, 11.6869, -1325.03]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_32"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2648.65, 12.4083, -4218.07]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=9
      distributionRadius:r=40
    }

    way{
      t2_inf_32_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2659.52, 11.745, -4187.6]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_32_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2682.59, 11.7282, -4158.99]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_33"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2739.14, 12.5426, -4214.02]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=40
    }

    way{
      t2_inf_33_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2722.35, 11.9967, -4207.77]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_34"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2739.14, 12.5426, -4146.96]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=40
    }

    way{
      t2_inf_34_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2729.42, 11.8071, -4138.64]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_34_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2711.83, 11.7686, -4143.37]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_35"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2604.14, 12.6612, -4324.05]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
      t2_inf_35_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2603.11, 12.554, -4292.67]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_35_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2566.61, 12.5837, -4263.66]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_36"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2644.74, 12.6612, -4313.3]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
      t2_inf_36_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2638.52, 12.5282, -4334.22]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_37"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2523.34, 12.6612, -4310.37]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
      t2_inf_37_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2547.37, 12.6022, -4261.37]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_38"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2495.52, 12.6612, -4252.34]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
      distributionRadius:r=20
    }

    way{
      t2_inf_38_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2492.18, 12.6624, -4285.92]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_inf_38_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2483.97, 12.6645, -4296.54]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_39"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2467.64, 12.6612, -4353.01]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
      t2_inf_39_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2425.87, 12.6665, -4344.99]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  infantry{
    name:t="t2_inf_40"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2511.61, 12.6612, -4529.79]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_41"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2493.21, 12.6612, -4510]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_42"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2417.13, 12.6612, -4434.25]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_43"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2367.65, 12.6612, -4399.27]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_44"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2663.38, 12.5295, -4517.4]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=2
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_45"
    tm:m=[[0.90172, 0, 0.43232] [0, 1, 0] [-0.43232, 0, 0.90172] [2529.95, 12.6612, -4568.04]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_46"
    tm:m=[[0.318092, 0, 0.948059] [0, 1, 0] [-0.948059, 0, 0.318092] [2732.32, 13.0722, -4815.69]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_47"
    tm:m=[[0.318092, 0, 0.948059] [0, 1, 0] [-0.948059, 0, 0.318092] [2692.11, 12.9093, -4802.2]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_48"
    tm:m=[[0.318092, 0, 0.948059] [0, 1, 0] [-0.948059, 0, 0.318092] [2665.1, 12.7956, -4801.61]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=3
    }

    way{
    }
  }

  tankModels{
    name:t="t2_tank_06"
    tm:m=[[0.942529, 0, -0.334124] [0, 1, 0] [0.334124, 0, 0.942529] [4224.15, 12.8572, -1707.81]]
    unit_class:t="ussr_t_62"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_tank_06_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4296.79, 13.1649, -1734.88]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_06_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4406.98, 13.0627, -1810.06]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_tank_06_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4435.8, 13.0263, -1829.77]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  armada{
    name:t="t1_heli_bot02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [39679.8, 1937.07, 2725.61]]
    unit_class:t="ah_1g"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t="ah_1g_rocket_ffar"
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=1
      count:i=1
      free_distance:r=70
      floating_distance:r=50
      minimum_distance_to_earth:r=20
      altLimit:r=200
      attack_type:t="fire_at_will"
      skill:i=4

      plane{
        wing_formation:t="Diamond"
        row_distances:r=3
        col_distances:r=3
        super_formation:t="Diamond"
        super_row_distances:r=1.5
        super_col_distances:r=1.5
        ai_skill:t="NORMAL"
        task:t="FLY_WAYPOINT"
      }
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa08"
    tm:m=[[0.924628, 0, 0.380872] [0, 1, 0] [-0.380872, 0, 0.924628] [8812.56, 50.8284, 298.19]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa09"
    tm:m=[[0.954032, 0, -0.299705] [0, 1, 0] [0.299705, 0, 0.954032] [8817.56, 49.3952, 318.99]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_19"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [8801.26, 49.6185, 309.07]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa10"
    tm:m=[[0.481086, 0, -0.876674] [0, 1, 0] [0.876674, 0, 0.481086] [14484.3, 257.15, 3637.92]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa11"
    tm:m=[[0.481086, 0, -0.876674] [0, 1, 0] [0.876674, 0, 0.481086] [11379.3, 191.633, -3373.94]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  squad{
    name:t="t2_inf_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [3914.35, 12.0811, -1538.38]]

    props{
      squad_members:t="t2_inf_28"
      squad_members:t="t2_inf_29"
      squad_members:t="t2_inf_11"
      squad_members:t="t2_inf_13"
      squad_members:t="t2_inf_21"
      squad_members:t="t2_inf_22"
      squad_members:t="t2_inf_23"
      squad_members:t="t2_inf_24"
      squad_members:t="t2_inf_30"
      squad_members:t="t2_inf_10"
      squad_members:t="t2_inf_09"
      squad_members:t="t2_inf_26"
      squad_members:t="t2_inf_25"
      squad_members:t="t2_inf_27"
      squad_members:t="t2_inf_31"
      squad_members:t="t2_inf_20"
    }
  }

  squad{
    name:t="t2_armored_units_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [4007.15, 11.5052, -1599.11]]

    props{
      squad_members:t="t2_inf_veh_11"
      squad_members:t="t2_inf_veh_13"
      squad_members:t="t2_inf_veh_09"
      squad_members:t="t2_tank_06"
      squad_members:t="t2_tank_05"
    }
  }

  squad{
    name:t="t2_inf_squad_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2558.1, 12.6377, -4468.26]]

    props{
      squad_members:t="t2_inf_04"
      squad_members:t="t2_inf_33"
      squad_members:t="t2_inf_34"
      squad_members:t="t2_inf_17"
      squad_members:t="t2_inf_32"
      squad_members:t="t2_inf_36"
      squad_members:t="t2_inf_35"
      squad_members:t="t2_inf_37"
      squad_members:t="t2_inf_38"
      squad_members:t="t2_inf_44"
      squad_members:t="t2_inf_01"
      squad_members:t="t2_inf_02"
      squad_members:t="t2_inf_03"
      squad_members:t="t2_inf_12"
      squad_members:t="t2_inf_39"
      squad_members:t="t2_inf_42"
      squad_members:t="t2_inf_43"
      squad_members:t="t2_inf_40"
      squad_members:t="t2_inf_41"
      squad_members:t="t2_inf_45"
      squad_members:t="t2_inf_05"
      squad_members:t="t2_inf_06"
      squad_members:t="t2_inf_16"
      squad_members:t="t2_inf_15"
      squad_members:t="t2_inf_46"
      squad_members:t="t2_inf_47"
      squad_members:t="t2_inf_48"
      squad_members:t="t2_inf_14"
      squad_members:t="t2_inf_07"
      squad_members:t="t2_inf_08"
    }
  }

  squad{
    name:t="t2_armored_units_squad_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2610.25, 12.5779, -4432.25]]

    props{
      squad_members:t="t2_inf_veh_02"
      squad_members:t="t2_inf_veh_12"
      squad_members:t="t2_inf_veh_01"
      squad_members:t="t2_tank_01"
      squad_members:t="t2_tank_02"
      squad_members:t="t2_tank_03"
      squad_members:t="t2_tank_04"
      squad_members:t="t2_inf_veh_03"
      squad_members:t="t2_inf_veh_04"
      squad_members:t="t2_inf_veh_05"
      squad_members:t="t2_inf_veh_06"
      squad_members:t="t2_inf_veh_07"
      squad_members:t="t2_inf_veh_08"
      squad_members:t="t2_spaa_01"
    }
  }

  ships{
    name:t="t2_gunboat_01"
    tm:m=[[0.737277, 0, -0.67559] [0, 1, 0] [0.67559, 0, 0.737277] [6677.27, 0, 3100.23]]
    unit_class:t="ussr_pr_1204_late"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=yes
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
      targetAir:b=yes
      accuracy:r=0.29
    }

    way{
      t2_gunboat_01_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [7548.04, 0, 2520.22]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_01_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [8323.22, 0, 1914.28]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_01_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [9393.13, 0, 1268.26]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_01_wp_07{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [10452.6, 0, 742.059]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_01_wp_08{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [10959.2, 0, 371.036]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_01_wp_09{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [11426.1, 0.00012207, 132.579]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  ships{
    name:t="t2_gunboat_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [6399.26, 0, 2670.25]]
    unit_class:t="ussr_pr_123k"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=yes
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
      targetAir:b=yes
      accuracy:r=0.34
    }

    way{
      t2_gunboat_02_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [7363.04, 0, 2633.81]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_02_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [8222.95, 0, 2053.46]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_02_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [9032, 0, 1386.75]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_gunboat_02_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [10313.5, 0, 1213.14]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  squad{
    name:t="gunboat_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [5944.04, 0, 2415.18]]

    props{
      squad_members:t="t2_gunboat_01"
      squad_members:t="t2_gunboat_02"
    }
  }

  ships{
    name:t="t2_boat_03"
    tm:m=[[0.906308, 0, 0.422618] [0, 1, 0] [-0.422618, 0, 0.906308] [12349.8, 0, -66.0896]]
    unit_class:t="ussr_pr_123k"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa13"
    tm:m=[[0.924628, 0, 0.380872] [0, 1, 0] [-0.380872, 0, 0.924628] [8812.56, 20.5766, 2417.68]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa14"
    tm:m=[[0.954032, 0, -0.299705] [0, 1, 0] [0.299705, 0, 0.954032] [8817.56, 21.6036, 2438.48]]
    unit_class:t="ussr_btr_152a"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  infantry{
    name:t="t2_inf_stationy_20"
    tm:m=[[0.717009, 0, -0.697064] [0, 1, 0] [0.697064, 0, 0.717009] [8801.26, 20.3232, 2428.56]]
    unit_class:t="cu_ru_modern_infantry"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      attack_type:t="fire_at_will"
      count:i=4
      distributionRadius:r=20
    }

    way{
    }
  }

  tankModels{
    name:t="t2_spaa12"
    tm:m=[[0.481086, 0, -0.876674] [0, 1, 0] [0.876674, 0, 0.481086] [14367.1, 124.462, 5569.59]]
    unit_class:t="ussr_zsu_23_4"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
    }
  }

  squad{
    name:t="t1_ground_units_squad"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25290, 100.357, 4515.83]]

    props{
      squad_members:t="t1_stationary_vehicles_01"
      squad_members:t="t1_stationary_vehicles_02"
      squad_members:t="t1_stationary_vehicles_03"
      squad_members:t="t1_stationary_vehicles_04"
      squad_members:t="t1_stationary_vehicles_05"
      squad_members:t="t1_stationary_vehicles_06"
      squad_members:t="t1_stationary_vehicles_07"
      squad_members:t="t1_stationary_vehicles_08"
      squad_members:t="t1_stationary_infantry_01"
      squad_members:t="t1_stationary_infantry_02"
      squad_members:t="t1_stationary_infantry_03"
      squad_members:t="t1_stationary_infantry_04"
      squad_members:t="t1_stationary_infantry_05"
      squad_members:t="t1_stationary_infantry_06"
      squad_members:t="t1_stationary_infantry_07"
      squad_members:t="t1_stationary_infantry_08"
      squad_members:t="t1_stationary_infantry_09"
      squad_members:t="t1_stationary_infantry_10"
      squad_members:t="t1_stationary_infantry_11"
      squad_members:t="t1_stationary_infantry_12"
      squad_members:t="t1_stationary_infantry_13"
      squad_members:t="t1_stationary_infantry_14"
      squad_members:t="t1_stationary_infantry_15"
      squad_members:t="t1_stationary_infantry_16"
      squad_members:t="t1_stationary_infantry_17"
      squad_members:t="t1_stationary_infantry_18"
      squad_members:t="t1_stationary_infantry_19"
      squad_members:t="t1_stationary_infantry_20"
      squad_members:t="t1_stationary_infantry_21"
      squad_members:t="t1_stationary_infantry_22"
      squad_members:t="t1_stationary_infantry_23"
      squad_members:t="t1_stationary_infantry_24"
    }
  }

  squad{
    name:t="t2_second_obj_veh_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [12701.6, 0, -202.763]]

    props{
      squad_members:t="t2_sec_veh_01"
      squad_members:t="t2_sec_veh_02"
      squad_members:t="t2_sec_veh_03"
      squad_members:t="t2_sec_veh_04"
      squad_members:t="t2_boat_01"
      squad_members:t="t2_boat_03"
      squad_members:t="t2_spaa05"
    }
  }

  tankModels{
    name:t="t2_sec_veh_01"
    tm:m=[[-0.375465, -0.167731, 0.911533] [-0.187523, 0.976896, 0.102517] [-0.907668, -0.132442, -0.398244] [13131.9, 11.5963, 409.354]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_sec_veh_01_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13115.8, 11.3644, 447.183]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_01_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13080.6, 10.3056, 497.164]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_01_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13043.7, 9.53081, 524.672]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_sec_veh_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13237.5, 18.9909, -360.266]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_sec_veh_02_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13307.1, 30.4242, -354.802]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_02_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13380.3, 41.7191, -351.174]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_02_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13399.3, 41.7063, -364.154]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_02_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13403.4, 41.6395, -373.063]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_02_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13402.7, 40.0066, -389.047]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_02_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13403.7, 38.0698, -412.248]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_sec_veh_03"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13264.8, 23.6295, -360.266]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_sec_veh_03_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13309.9, 29.9456, -367.018]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13313.7, 29.874, -375.931]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13308.8, 28.178, -388.953]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13306, 26.5756, -405.18]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13306.6, 24.9666, -428.381]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13323.4, 27.1878, -432.643]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_07{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13335.1, 29.4834, -425.554]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_08{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13348.1, 31.9637, -418.472]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_09{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13361.2, 33.7802, -411.897]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_10{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13372.1, 34.9341, -408.575]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_11{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13377.7, 35.1258, -410.614]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_12{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13378.5, 34.1455, -420.201]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_03_wp_13{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13385.2, 32.5767, -439.334]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  tankModels{
    name:t="t2_sec_veh_04"
    tm:m=[[-0.169273, -0.167731, 0.971191] [-0.160889, 0.976896, 0.140674] [-0.972348, -0.132442, -0.192348] [13134.8, 11.5963, 398.156]]
    unit_class:t="ussr_bmp_1"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      formation_type:t="rows"
      formation_div:i=3
      formation_step:p2=2.5, 2
      formation_noise:p2=0.1, 0.1
      uniqueName:t=""
      attack_type:t="fire_at_will"
    }

    way{
      t2_sec_veh_04_wp_01{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13165.8, 11.69, 397.177]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_04_wp_02{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13182.3, 12.1832, 440.563]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_04_wp_03{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13169.7, 11.4836, 482.29]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_04_wp_04{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13143.3, 10.6371, 523.762]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_04_wp_05{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13124, 10.3005, 533.05]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }

      t2_sec_veh_04_wp_06{
        type:t="normal"
        tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [13102, 10.0307, 535.137]]

        props{
          speed:r=300
          tas:b=no
          moveType:t="MOVETO_STRAIGHT"
          shouldKeepFormation:b=no
          canUsePathFinder:b=no
        }
      }
    }
  }

  squad{
    name:t="t2_second_obj_inf_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [12637.1, 0, -7.57028]]

    props{
      squad_members:t="t2_inf_stationy_08"
      squad_members:t="t2_inf_stationy_09"
      squad_members:t="t2_inf_stationy_10"
      squad_members:t="t2_inf_stationy_07"
      squad_members:t="t2_inf_stationy_03"
      squad_members:t="t2_inf_stationy_04"
      squad_members:t="t2_inf_stationy_12"
      squad_members:t="t2_inf_stationy_05"
      squad_members:t="t2_inf_stationy_06"
      squad_members:t="t2_inf_stationy_13"
      squad_members:t="t2_inf_stationy_02"
      squad_members:t="t2_inf_stationy_14"
      squad_members:t="t2_inf_stationy_15"
      squad_members:t="t2_inf_stationy_16"
      squad_members:t="t2_inf_stationy_01"
      squad_members:t="t2_inf_stationy_18"
      squad_members:t="t2_inf_stationy_17"
    }
  }

  squad{
    name:t="panic_squad_02"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [3862.44, 11.0375, -1808.78]]

    props{
      squad_members:t="t2_tank_05"
      squad_members:t="t2_inf_veh_09"
      squad_members:t="t2_inf_veh_11"
      squad_members:t="t2_inf_09"
      squad_members:t="t2_inf_10"
      squad_members:t="t2_inf_11"
      squad_members:t="t2_inf_veh_13"
      squad_members:t="t2_inf_13"
      squad_members:t="t2_inf_20"
      squad_members:t="t2_inf_21"
      squad_members:t="t2_inf_22"
      squad_members:t="t2_inf_23"
      squad_members:t="t2_inf_24"
      squad_members:t="t2_inf_25"
      squad_members:t="t2_inf_26"
      squad_members:t="t2_inf_27"
      squad_members:t="t2_inf_28"
      squad_members:t="t2_inf_29"
      squad_members:t="t2_inf_30"
      squad_members:t="t2_inf_31"
      squad_members:t="t2_tank_06"
    }
  }

  squad{
    name:t="panic_squad_03"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [2329.82, 12.6658, -4592.47]]

    props{
      squad_members:t="t2_spaa_01"
      squad_members:t="t2_tank_01"
      squad_members:t="t2_tank_02"
      squad_members:t="t2_tank_03"
      squad_members:t="t2_tank_04"
      squad_members:t="t2_inf_01"
      squad_members:t="t2_inf_02"
      squad_members:t="t2_inf_03"
      squad_members:t="t2_inf_veh_01"
      squad_members:t="t2_inf_veh_02"
      squad_members:t="t2_inf_04"
      squad_members:t="t2_inf_veh_03"
      squad_members:t="t2_inf_veh_04"
      squad_members:t="t2_inf_veh_05"
      squad_members:t="t2_inf_veh_06"
      squad_members:t="t2_inf_veh_07"
      squad_members:t="t2_inf_veh_08"
      squad_members:t="t2_inf_05"
      squad_members:t="t2_inf_06"
      squad_members:t="t2_inf_07"
      squad_members:t="t2_inf_08"
      squad_members:t="t2_inf_veh_12"
      squad_members:t="t2_inf_12"
      squad_members:t="t2_inf_14"
      squad_members:t="t2_inf_15"
      squad_members:t="t2_inf_16"
      squad_members:t="t2_inf_17"
      squad_members:t="t2_inf_32"
      squad_members:t="t2_inf_33"
      squad_members:t="t2_inf_34"
      squad_members:t="t2_inf_35"
      squad_members:t="t2_inf_36"
      squad_members:t="t2_inf_37"
      squad_members:t="t2_inf_38"
      squad_members:t="t2_inf_39"
      squad_members:t="t2_inf_40"
      squad_members:t="t2_inf_41"
      squad_members:t="t2_inf_42"
      squad_members:t="t2_inf_43"
      squad_members:t="t2_inf_44"
      squad_members:t="t2_inf_45"
      squad_members:t="t2_inf_46"
      squad_members:t="t2_inf_47"
      squad_members:t="t2_inf_48"
    }
  }

  squad{
    name:t="panic_squad_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [12872.6, 6.5022, -40.6696]]

    props{
      squad_members:t="t2_inf_stationy_01"
      squad_members:t="t2_inf_stationy_02"
      squad_members:t="t2_inf_stationy_14"
      squad_members:t="t2_inf_stationy_15"
      squad_members:t="t2_inf_stationy_16"
      squad_members:t="t2_inf_stationy_17"
      squad_members:t="t2_inf_stationy_18"
      squad_members:t="t2_sec_veh_01"
      squad_members:t="t2_sec_veh_04"
      squad_members:t="t2_inf_stationy_03"
      squad_members:t="t2_inf_stationy_04"
      squad_members:t="t2_inf_stationy_05"
      squad_members:t="t2_inf_stationy_06"
      squad_members:t="t2_inf_stationy_07"
      squad_members:t="t2_inf_stationy_12"
      squad_members:t="t2_inf_stationy_13"
      squad_members:t="t2_sec_veh_02"
      squad_members:t="t2_sec_veh_03"
      squad_members:t="t2_inf_stationy_08"
      squad_members:t="t2_inf_stationy_09"
      squad_members:t="t2_inf_stationy_10"
    }
  }
}

areas{
  battlearea_01{
    type:t="Box"
    tm:m=[[65536, 0, 0] [0, 2048, 0] [0, 0, 65536] [-26.3865, 0, 0]]
    objLayer:i=0

    props{
    }
  }

  t1_helipad_area_01{
    type:t="Point"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25368.3, 94.1691, 4665.71]]
    objLayer:i=0

    props{
    }
  }

  t1_helipad_area_02{
    type:t="Point"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [25158.8, 92.5384, 4665.16]]
    objLayer:i=0

    props{
    }
  }

  t1_helipad_spawn_01{
    type:t="Sphere"
    tm:m=[[39.9996, 0, -0.179621] [0, 40, 0] [0.179621, 0, 39.9996] [25300.9, 94.5556, 4730.96]]
    objLayer:i=0

    props{
    }
  }

  t1_helipad_spawn_02{
    type:t="Sphere"
    tm:m=[[40, 0, 0] [0, 40, 0] [0, 0, 40] [25213.4, 94.2315, 4730.11]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_01{
    type:t="Sphere"
    tm:m=[[511.526, 0, -3563.47] [0, 416.508, 0] [402.644, 0, 57.798] [22830.2, 216.214, 5524.82]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_02{
    type:t="Sphere"
    tm:m=[[2325.79, -234.075, -8631.08] [1.4317, 210.136, -5.31308] [473.803, 0, 127.674] [20749.9, 282.786, 5884.16]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_04{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [3.54269, 329.806, -4.52564] [442.081, 0, 346.064] [18185.2, 267.163, 4814.83]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_01{
    type:t="Cylinder"
    tm:m=[[600, 0, 0] [0, 400, 0] [0, 0, 600] [3991.64, 353.085, -4067.1]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_02{
    type:t="Cylinder"
    tm:m=[[1200, 0, 0] [0, 400, 0] [0, 0, 1200] [4675.28, 353.085, -5320.74]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_03{
    type:t="Cylinder"
    tm:m=[[1200, 0, 0] [0, 400, 0] [0, 0, 1200] [5667.23, 353.085, -6109.95]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_04{
    type:t="Cylinder"
    tm:m=[[1000, 0, 0] [0, 300, 0] [0, 0, 1000] [5399.36, 178.086, -1364.85]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_05{
    type:t="Cylinder"
    tm:m=[[1000, 0, 0] [0, 300, 0] [0, 0, 1000] [4613.81, 178.086, -1440.22]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_06{
    type:t="Cylinder"
    tm:m=[[1000, 0, 0] [0, 300, 0] [0, 0, 1000] [3833.6, 178.086, -1526.32]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_07{
    type:t="Cylinder"
    tm:m=[[1200, 0, 0] [0, 400, 0] [0, 0, 1200] [7471.04, 353.085, -3878.77]]
    objLayer:i=0

    props{
    }
  }

  all_spot_area_08{
    type:t="Cylinder"
    tm:m=[[1200, 0, 0] [0, 400, 0] [0, 0, 1200] [8182.67, 353.085, -3041.61]]
    objLayer:i=0

    props{
    }
  }

  t1_helipad_spawn_03{
    type:t="Sphere"
    tm:m=[[40, 0, 0] [0, 40, 0] [0, 0, 40] [25189.7, 94.2315, 4667.21]]
    objLayer:i=0

    props{
    }
  }

  helipad_waypoint_01{
    type:t="Sphere"
    tm:m=[[800, 0, 0] [0, 800, 0] [0, 0, 800] [25291.7, 215.679, 4644.7]]
    objLayer:i=0

    props{
    }
  }

  exit_waypoint_01{
    type:t="Sphere"
    tm:m=[[800, 0, 0] [0, 800, 0] [0, 0, 800] [11114, 215.679, 2589.58]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_03{
    type:t="Sphere"
    tm:m=[[5012.68, -390.081, -10064.1] [6.30951, 407.908, -12.6678] [439.235, 0, 218.773] [19501.9, 349.674, 5564.44]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_05{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [2.08787, 194.37, -2.66717] [442.081, 0, 346.064] [17104.1, 152.561, 3816.59]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_06{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [2.08787, 194.37, -2.66717] [442.081, 0, 346.064] [16097.5, 123.789, 3029.24]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_07{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [2.08787, 194.37, -2.66717] [442.081, 0, 346.064] [15075.1, 90.6875, 1417.59]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_08{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [2.08787, 194.37, -2.66717] [442.081, 0, 346.064] [13576.8, 79.7752, 1061.43]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_09{
    type:t="Sphere"
    tm:m=[[6244.3, -67.6841, -7974.11] [-1.29911, 194.377, -2.66717] [442.014, 7.70272, 346.064] [11129.5, 64.8543, -794.761]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_10{
    type:t="Sphere"
    tm:m=[[6242.17, -176.473, -7974.11] [2.08787, 194.37, -2.66717] [442.081, 0, 346.064] [9654.52, 64.8543, -1949.41]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_11{
    type:t="Sphere"
    tm:m=[[4186.09, -171.499, -9221.15] [4.34353, 404.361, -5.54869] [511.192, -2.30608, 232.107] [8173.46, 89.5254, -1310.88]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_12{
    type:t="Sphere"
    tm:m=[[-2566.75, 11.3894, -1179.26] [2.08787, 194.37, -2.66717] [234.317, -9.51658, -510.099] [7100.45, 364.547, 125.226]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_13{
    type:t="Sphere"
    tm:m=[[277.131, 197.001, -1846.33] [-1.3655, 193.32, 20.422] [555.258, -4.82786, 82.8282] [5919.05, 197.973, 544.054]]
    objLayer:i=0

    props{
    }
  }

  waypoint_01_14{
    type:t="Sphere"
    tm:m=[[564.074, 192.053, -1780.3] [-1.3655, 193.32, 20.422] [535.468, -13.981, 168.15] [4816.88, 48.6528, 362.687]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_01{
    type:t="Box"
    tm:m=[[6000, 0, 0] [0, 3000, 0] [0, 0, 6000] [24543.1, 0, 4964.68]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_02{
    type:t="Box"
    tm:m=[[6000, 0, 0] [0, 3000, 0] [0, 0, 6000] [19943.8, 0, 4964.68]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_03{
    type:t="Box"
    tm:m=[[4732.46, 0, 3688.34] [0, 3000, 0] [-4303.07, 0, 5521.2] [17448.8, 0, 4196.01]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_04{
    type:t="Box"
    tm:m=[[5249.46, 0, 2905.71] [0, 3000, 0] [-3390, 0, 6124.37] [13704, 0, 1643.44]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_05{
    type:t="Box"
    tm:m=[[5249.46, 0, 2905.71] [0, 3000, 0] [-3390, 0, 6124.37] [9098.44, 0, -872.652]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_06{
    type:t="Box"
    tm:m=[[5249.46, 0, 2905.71] [0, 3000, 0] [-3390, 0, 6124.37] [4066.55, 0, -3657.93]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_07{
    type:t="Box"
    tm:m=[[5249.46, 0, 2905.71] [0, 3000, 0] [-3390, 0, 6124.37] [6513.05, 0, -8077.79]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_08{
    type:t="Box"
    tm:m=[[5739.39, 0, -1749.11] [0, 3000, 0] [2040.63, 0, 6695.96] [9232.03, 0, -5290.04]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_09{
    type:t="Box"
    tm:m=[[5739.39, 0, -1749.11] [0, 3000, 0] [2040.63, 0, 6695.96] [3245.7, 0, -264.432]]
    objLayer:i=0

    props{
    }
  }

  mission_battlearea_10{
    type:t="Box"
    tm:m=[[9982.75, 0, 587.111] [0, 3000, 0] [-234.844, 0, 3993.1] [6608.9, 0, 2333.29]]
    objLayer:i=0

    props{
    }
  }

  boat_fire_area{
    type:t="Sphere"
    tm:m=[[1259.6, 0, 1074.48] [0, 159.189, 0] [-752.365, 0, 881.99] [12565.1, 53.9884, 479.979]]
    objLayer:i=0

    props{
    }
  }

  boat_fire_area01{
    type:t="Sphere"
    tm:m=[[1655.07, 0, -42.7536] [0, 159.189, 0] [29.9366, 0, 1158.91] [12201, 53.9884, -94.5145]]
    objLayer:i=0

    props{
    }
  }

  boat_fire_area02{
    type:t="Sphere"
    tm:m=[[1489.02, 0, -723.815] [0, 159.189, 0] [506.827, 0, 1042.63] [11606.2, 53.9884, 11.8681]]
    objLayer:i=0

    props{
    }
  }

  enemy_waypoint_01{
    type:t="Sphere"
    tm:m=[[20, 0, 0] [0, 20, 0] [0, 0, 20] [4004.15, 153, -1540.65]]
    objLayer:i=0

    props{
    }
  }

  enemy_waypoint_02{
    type:t="Sphere"
    tm:m=[[20, 0, 0] [0, 20, 0] [0, 0, 20] [2621.16, 153, -4564.05]]
    objLayer:i=0

    props{
    }
  }

  checkpoint_01{
    type:t="Sphere"
    tm:m=[[-4.83718, 0, -3.54989] [0, 6, 0] [3.54989, 0, -4.83718] [14055.5, 65.8141, 1523.38]]
    objLayer:i=0

    props{
    }
  }

  checkpoint_02{
    type:t="Sphere"
    tm:m=[[-5.65501, 0, -2.00522] [0, 6, 0] [2.00522, 0, -5.65501] [4614.06, 19.6397, 363.647]]
    objLayer:i=0

    props{
    }
  }

  checkpoint_03{
    type:t="Sphere"
    tm:m=[[5.60347, 0, -2.14501] [0, 6, 0] [2.14501, 0, 5.60347] [6250.89, 147.466, -3350.18]]
    objLayer:i=0

    props{
    }
  }

  checkpoint_00{
    type:t="Sphere"
    tm:m=[[-39.8317, 0, 3.66513] [0, 40, 0] [-3.66513, 0, -39.8317] [24817.9, 130.87, 4775.4]]
    objLayer:i=0

    props{
    }
  }

  airfield_marker{
    type:t="Sphere"
    tm:m=[[-39.8317, 0, 3.66513] [0, 40, 0] [-3.66513, 0, -39.8317] [25476.2, 130.87, 4971.68]]
    objLayer:i=0

    props{
    }
  }

  player_shot_area_01{
    type:t="Sphere"
    tm:m=[[2400, 0, 0] [0, 2400, 0] [0, 0, 2400] [12700, 77.2852, 0]]
    objLayer:i=0

    props{
    }
  }

  player_shot_area_02{
    type:t="Sphere"
    tm:m=[[1600, 0, 0] [0, 1600, 0] [0, 0, 1600] [4204.87, 52.38, -1389.27]]
    objLayer:i=0

    props{
    }
  }

  player_shot_area_03{
    type:t="Sphere"
    tm:m=[[1600, 0, 0] [0, 1600, 0] [0, 0, 1600] [2553.03, 31.1487, -4570.08]]
    objLayer:i=0

    props{
    }
  }
}

objLayers{
  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }
}

wayPoints{
}
selected_tag:t=""
bin_dump_file:t=""

mission_settings{
  atmosphere{
    pressure:r=760
    temperature:r=15
  }

  stars{
    latitude:r=48
    longitude:r=44
    year:i=1940
    month:i=1
    day:i=15
    time:r=12
  }

  player{
    army:i=1
    wing:t="armada_01"
  }

  player_teamB{
    army:i=2
  }

  mission{
    name:t="test_plane_sample"
    level:t="levels/water.bin"
    type:t="singleMission"
    restoreType:t="attempts"
    optionalTakeOff:b=no
    campaign:t="UserMissions"
    environment:t="Day"
    weather:t="good"
    missionDebriefing:t=""
    missionBriefing:t=""
    difficulty:t="arcade"
    unlockGUID:t=""

    tags{
    }

    missionType{
      _Dom:b=no
      _Conq:b=no
      _CnvA:b=no
      _CnvB:b=no
      _ArtDA:b=no
      _ArtDB:b=no
      _Bttl:b=no
      _DBttlA:b=no
      _DBttlB:b=no
      _Bto:b=no
      _Flc:b=no
      _v1_race_straight:b=no
      _v1_race_inverted:b=no
      _v2_race_straight:b=no
      _v2_race_inverted:b=no
      _Conq1:b=no
      _Conq2:b=no
      _Conq3:b=no
      _Conq4:b=no
      _Conq5:b=no
      _Conq6:b=no
    }
  }

  spectator_points{
  }

  cover_points{
  }

  aiParams{
    aiEffectivenessViscosity:r=90
    effectivenessDistances:p2=2500, 7000
  }
}

imports{
}

triggers{
  isCategory:b=yes
  is_enabled:b=yes
}

mission_objectives{
  isCategory:b=yes
  is_enabled:b=yes
}

variables{
}

dialogs{
}

airfields{
}

effects{
}

units{
  armada{
    name:t="armada_01"
    tm:m=[[1, 0, 0] [0, 1, 0] [0, 0, 1] [0.9, 1000.24, -0.892]]
    unit_class:t="sample_i_185_m82"
    objLayer:i=1
    closed_waypoints:b=no
    isShipSpline:b=no
    shipTurnRadius:r=100
    weapons:t=""
    bullets0:t=""
    bullets1:t=""
    bullets2:t=""
    bullets3:t=""
    bulletsCount0:i=0
    bulletsCount1:i=0
    bulletsCount2:i=0
    bulletsCount3:i=0

    props{
      army:i=2
      count:i=1
      free_distance:r=70
      floating_distance:r=50
      minimum_distance_to_earth:r=20
      altLimit:r=6000
      attack_type:t="fire_at_will"
      skill:i=4

      plane{
        wing_formation:t="Diamond"
        row_distances:r=3
        col_distances:r=3
        super_formation:t="Diamond"
        super_row_distances:r=1.5
        super_col_distances:r=1.5
        ai_skill:t="NORMAL"
        task:t="FLY_WAYPOINT"
      }
    }

    way{
    }
  }
}

areas{
}

objLayers{
  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }

  layer{
    enabled:b=yes
  }
}

wayPoints{
}
