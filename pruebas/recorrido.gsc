#include maps\mp\_utility;
#include common_scripts\utility;

// Automatic tour used to test the minimap. Host only.
// Console, inside Origins: set mm_recorrido 1   (stop: set mm_recorrido 0)
// Writes "MMTOUR <step>" lines to games_mp.log so a recording can be indexed.
init()
{
	if ( getdvar( "mm_recorrido" ) == "" )
		setdvar( "mm_recorrido", "0" );
	level thread tour_wait();
}

tour_wait()
{
	level endon( "end_game" );
	wait 5;
	for ( ;; )
	{
		wait 1;
		if ( getdvarint( "mm_recorrido" ) != 1 )
			continue;
		players = get_players();
		if ( players.size == 0 || !isalive( players[ 0 ] ) || players[ 0 ].sessionstate != "playing" )
			continue;
		tour_run( players[ 0 ] );
		setdvar( "mm_recorrido", "0" );
		setdvar( "mm_big", "0" );
	}
}

tour_on()
{
	return getdvarint( "mm_recorrido" ) == 1;
}

tour_log( text )
{
	logprint( "MMTOUR " + text + "\n" );
}

tour_run( me )
{
	me endon( "disconnect" );
	level.player_out_of_playable_area_monitor = 0;
	me notify( "stop_player_out_of_playable_area_monitor" );
	me enableinvulnerability();
	me.ignoreme = 1;
	me freezecontrols( 1 );
	tour_log( "inicio" );
	wait 3;

	tour_stop( me, ( 2728, 5320, -352 ), "laboratorio" );
	tour_big( me, "mapa grande laboratorio" );
	tour_stop( me, ( 2240, 4672, -299 ), "g1" );
	tour_stop( me, ( 1952, 3632, -309 ), "trinchera este" );
	tour_stop( me, ( 2918, 4442, -579 ), "cueva fuego" );
	tour_stop( me, ( -288, 3520, -291 ), "g2" );
	tour_stop( me, ( -752, 2816, -111 ), "bunker oeste" );
	tour_stop( me, ( 448, 2240, -121 ), "g3" );
	tour_stop( me, ( -1536, 2432, 16 ), "camino del tanque" );
	tour_stop( me, ( 120, -256, 320 ), "mid" );
	tour_stop( me, ( -256, 0, 40 ), "cripta arriba" );
	tour_stop( me, ( 64, -192, -688 ), "cripta abajo" );
	tour_big( me, "mapa grande cripta" );
	tour_stop( me, ( 3376, 1246, -347 ), "cueva viento" );
	tour_stop( me, ( 2304, 128, 120 ), "g4" );
	tour_stop( me, ( -3192, -274, -173 ), "cueva rayo" );
	tour_stop( me, ( -2552, 112, 236 ), "g5" );
	tour_stop( me, ( 1408, -1664, -123 ), "cueva hielo" );
	tour_stop( me, ( 417, -2711, 116 ), "iglesia abajo" );
	tour_stop( me, ( 640, -2688, 339 ), "iglesia arriba" );
	tour_stop( me, ( 896, -3712, 306 ), "g6" );
	tour_stop( me, ( 10368, -7936, -411 ), "crazy place centro" );
	tour_big( me, "mapa grande crazy place" );
	tour_stop( me, ( 9600, -7040, -345 ), "crazy place portal rayo" );
	tour_stop( me, ( 11264, -8576, -413 ), "crazy place portal viento" );

	if ( tour_on() )
		tour_panzer( me );
	if ( tour_on() )
		tour_attack( me );
	if ( tour_on() )
		tour_robots( me );

	tour_log( "fin" );
	me freezecontrols( 0 );
	me.ignoreme = 0;
	iprintlnbold( "Recorrido terminado" );
}

// go there, then one full turn in about 5 seconds
tour_stop( me, org, name )
{
	if ( !tour_on() )
		return;
	me setorigin( org + ( 0, 0, 8 ) );
	me setplayerangles( ( 0, 90, 0 ) );
	tour_log( name );
	iprintln( "^3" + name );
	wait 2;
	tour_turn( me );
	wait 0.5;
}

tour_turn( me )
{
	for ( i = 0; i < 100; i++ )
	{
		yaw = 90 + i * 3.6;
		if ( yaw > 180 )
			yaw -= 360;
		me setplayerangles( ( 0, yaw, 0 ) );
		wait 0.05;
	}
}

tour_big( me, name )
{
	if ( !tour_on() )
		return;
	tour_log( name );
	setdvar( "mm_big", "1" );
	wait 4;
	setdvar( "mm_big", "0" );
	wait 0.5;
}

tour_panzer( me )
{
	me setorigin( ( -1216, 704, 111 ) );
	tour_log( "panzer pedido" );
	// the Panzer only appears in zones that are open
	zones = strtok( "zone_nml_0 zone_nml_1 zone_nml_2 zone_nml_3 zone_nml_4 zone_nml_5 zone_nml_6 zone_nml_18 zone_nml_19", " " );
	for ( i = 0; i < zones.size; i++ )
	{
		if ( isdefined( level.zones[ zones[ i ] ] ) )
			maps\mp\zombies\_zm_zonemgr::enable_zone( zones[ i ] );
	}
	wait 3;
	for ( i = 0; i < 30; i++ )
	{
		if ( i % 6 == 0 )
		{
			level.mechz_left_to_spawn = 1;
			level notify( "spawn_mechz" );
			if ( isdefined( level.zombie_mechz_locations ) )
				tour_log( "lugares de panzer " + level.zombie_mechz_locations.size );
		}
		wait 1;
		if ( tour_has_panzer() )
		{
			tour_log( "panzer visible" );
			tour_turn( me );
			tour_big( me, "mapa grande panzer" );
			return;
		}
	}
	tour_log( "panzer no aparecio" );
}

tour_has_panzer()
{
	foreach ( ai in getaiarray( level.zombie_team ) )
	{
		if ( isdefined( ai ) && isalive( ai ) && isdefined( ai.is_mechz ) && ai.is_mechz )
			return 1;
	}
	return 0;
}

// gives the first two generators with the game's own function, then starts a real attack round
tour_attack( me )
{
	if ( !isdefined( level.zone_capture ) || !isdefined( level.zone_capture.zones ) )
	{
		tour_log( "sin generadores" );
		return;
	}
	done = 0;
	foreach ( zone in level.zone_capture.zones )
	{
		if ( done >= 2 )
			break;
		zone.n_current_progress = 100;
		zone maps\mp\zm_tomb_capture_zones::handle_generator_capture();
		tour_log( "capturado " + zone.script_noteworthy );
		done++;
		wait 1;
	}
	tour_stop( me, ( 448, 2240, -121 ), "generadores verdes" );
	tour_big( me, "mapa grande generadores" );
	tour_log( "ataque pedido" );
	level thread maps\mp\zm_tomb_capture_zones::recapture_round_start();
	for ( i = 0; i < 9; i++ )
	{
		wait 4;
		tour_log( "estado " + getdvar( "mm_gen" ) );
		if ( i == 3 )
			tour_big( me, "mapa grande ataque" );
	}
}

// waits next to a stomp zone until a robot walks by
tour_robots( me )
{
	me setorigin( ( -1216, 704, 111 ) );
	tour_log( "esperando robot" );
	for ( i = 0; i < 60; i++ )
	{
		wait 1;
		if ( getdvar( "mm_feet" ) != "" )
		{
			tour_log( "robot caminando" );
			tour_turn( me );
			tour_turn( me );
			tour_big( me, "mapa grande robot" );
			return;
		}
	}
	tour_log( "no paso ningun robot" );
}
