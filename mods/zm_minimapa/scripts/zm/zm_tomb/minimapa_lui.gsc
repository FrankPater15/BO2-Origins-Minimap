#include maps\mp\_utility;
#include common_scripts\utility;

// Publishes host position + nearby enemies to dvars read by hudtimerzombie.lua.
// Listen-server host only. Console: minimapa_lui 0/1
init()
{
	precacheshader( "white" );
	precacheshader( "menu_lobby_icon_twitter" );
	precacheshader( "zombies_rank_5" );
	precacheshader( "specialty_juggernaut_zombies" );
	precacheshader( "specialty_quickrevive_zombies" );
	precacheshader( "specialty_fastreload_zombies" );
	precacheshader( "specialty_marathon_zombies" );
	precacheshader( "specialty_additionalprimaryweapon_zombies" );
	precacheshader( "menu_lobby_icon_facebook" );
	precacheshader( "zombies_rank_3_ded" );
	precacheshader( "zombies_rank_4_ded" );
	precacheshader( "zombies_rank_5_ded" );
	setdvar( "mm_zone", "" );
	if ( getdvar( "mm_giro" ) == "" )
		setdvar( "mm_giro", "1" ); // 0 plain, 1 compensate rotation delay, 2 container
	setdvar( "mm_big", "0" ); // full map, key M
	setdvar( "mm_ay", "" );
	if ( getdvar( "minimapa_lui" ) == "" )
		setdvar( "minimapa_lui", "1" );
	setdvar( "minimapa", "0" ); // hide the old fixed hudelem map
	if ( getdvar( "mm_rotsign" ) == "" )
		setdvar( "mm_rotsign", "1" );
	if ( getdvar( "mm_smooth" ) == "" )
		setdvar( "mm_smooth", "0" );
	if ( getdvar( "mm_zoom" ) == "" )
		setdvar( "mm_zoom", "1750" );
	setdvar( "mm_state", "0 0 0 0 0" );
	for ( k = 0; k < 4; k++ )
		setdvar( "mm_e" + k, "" );
	level.mml_cells = [];
	level.mml_parts = [];
	level thread mml_cells_setup();
	level thread mml_loop();
	level thread mml_end();
	level thread mml_diag();
	level thread mml_info();
	level thread mml_poi();
	level thread mml_feet();
	level thread mml_zone();
}

mml_loop()
{
	level endon( "end_game" );
	seq = 0;
	under = 0;
	same = 0;
	for ( ;; )
	{
		wait 0.05;
		players = get_players();
		if ( players.size == 0 || !isdefined( players[ 0 ] ) )
			continue;
		seq = ( seq + 1 ) % 1000;
		me = players[ 0 ]; // expected to be the host; test in co-op
		visible = getdvarint( "minimapa_lui" ) == 1 && isalive( me ) && me.sessionstate == "playing" && mml_inside( me.origin );
		if ( !visible )
		{
			setdvar( "mm_state", seq + " 0 0 0 0" );
			continue;
		}
		now = mml_under( me.origin );
		if ( now == under )
			same = 0;
		else
			same++;
		if ( same >= 5 )
		{
			under = now;
			same = 0;
		}
		angles = me getplayerangles();
		mml_entities( me, players );
		// written last: Lua redraws when this one changes
		setdvar( "mm_state", seq + " 1 " + int( me.origin[ 0 ] ) + " " + int( me.origin[ 1 ] ) + " " + int( angles[ 1 ] * 10 ) + " " + under );
	}
}

mml_end()
{
	level waittill( "end_game" );
	setdvar( "mm_big", "0" );
	setdvar( "mm_state", "0 0 0 0 0" );
}

mml_entities( me, players )
{
	out = [];
	for ( k = 0; k < 4; k++ )
		out[ k ] = "";
	count = 0;
	big = getdvarint( "mm_big" );
	team = "axis";
	if ( isdefined( level.zombie_team ) )
		team = level.zombie_team;
	foreach ( ai in getaiarray( team ) )
	{
		if ( count >= 24 )
			break;
		if ( !isdefined( ai ) || !isalive( ai ) || isdefined( ai.is_giant_robot ) )
			continue;
		dx = ai.origin[ 0 ] - me.origin[ 0 ];
		dy = ai.origin[ 1 ] - me.origin[ 1 ];
		// square map: 1750 * sqrt(2) reaches the corners
		if ( big != 1 && dx * dx + dy * dy > 12500000 )
			continue;
		dz = ai.origin[ 2 ] - me.origin[ 2 ];
		h = 0;
		if ( dz > 100 )
			h = 1;
		else if ( dz < -100 )
			h = 2;
		if ( isdefined( ai.is_mechz ) && ai.is_mechz )
			h = 4;
		k = int( count / 8 );
		out[ k ] = out[ k ] + int( ai.origin[ 0 ] ) + "," + int( ai.origin[ 1 ] ) + "," + h + "," + ai getentitynumber() + ";";
		count++;
	}
	yaws = "";
	foreach ( player in players )
	{
		if ( player == me || !isalive( player ) )
			continue;
		out[ 3 ] = out[ 3 ] + int( player.origin[ 0 ] ) + "," + int( player.origin[ 1 ] ) + ",3," + player getentitynumber() + ";";
		pa = player getplayerangles();
		yaws = yaws + player getentitynumber() + "," + int( pa[ 1 ] ) + ";";
	}
	for ( k = 0; k < 4; k++ )
		setdvar( "mm_e" + k, out[ k ] );
	setdvar( "mm_ay", yaws );
}

mml_key( x, y )
{
	return x + "_" + y;
}

mml_under( org )
{
	// 100 unit cells; the offset keeps the values positive
	k = mml_key( int( ( org[ 0 ] + 20000 ) / 100 ), int( ( org[ 1 ] + 20000 ) / 100 ) );
	if ( isdefined( level.mml_cells[ k ] ) && org[ 2 ] < level.mml_cells[ k ] )
		return level.mml_parts[ k ];
	k = k + "b";
	if ( isdefined( level.mml_cells[ k ] ) && org[ 2 ] < level.mml_cells[ k ] )
		return level.mml_parts[ k ];
	return 0;
}

// "x,y,z,part;..." a second entry of a cell is the higher one
mml_row( row )
{
	list = strtok( row, ";" );
	for ( i = 0; i < list.size; i++ )
	{
		v = strtok( list[ i ], "," );
		k = v[ 0 ] + "_" + v[ 1 ];
		if ( isdefined( level.mml_cells[ k ] ) )
			k = k + "b";
		level.mml_cells[ k ] = int( v[ 2 ] );
		level.mml_parts[ k ] = int( v[ 3 ] );
	}
	wait 0.05;
}

mml_cells_setup()
{
	mml_row( "171,201,306,10;171,202,306,10;172,200,126,10;172,201,306,10;172,202,306,10;173,200,150,10;173,201,150,10;173,202,150,10;173,203,145,10;174,195,78,10;174,196,90,10;174,197,122,10;174,198,152,10;174,199,162,10;174,200,162,10;174,201,162,10;174,202,162,10;175,195,78,10;175,196,90,10;175,197,128,10;175,198,158,10;175,199,162,10;175,200,162,10;175,201,162,10;175,202,162,10" );
	mml_row( "175,203,162,10;176,195,78,10;176,196,78,10;176,200,162,10;176,201,162,10;176,202,162,10;177,195,78,10;177,196,78,10;187,225,-42,8;187,226,-42,8;187,227,-42,8;187,228,-186,8;188,225,-42,8;188,226,-42,8;188,227,-42,8;188,228,-186,8;189,226,-42,8;189,227,-42,8;190,223,-186,8;190,224,-42,8;190,225,-42,8;190,226,-42,8;190,227,-42,8;190,228,-42,8;190,229,-42,8" );
	mml_row( "190,230,-42,8;190,231,-186,8;191,223,-42,8;191,224,-42,8;191,225,-42,8;191,226,-42,8;191,227,-42,8;191,228,-42,8;191,229,-42,8;191,230,-42,8;191,231,-186,8;192,222,-42,8;192,223,-42,8;192,224,-42,8;192,225,-42,8;192,226,-114,8;192,227,-66,8;192,228,-30,8;192,229,-42,8;192,230,-42,8;192,231,-42,8;193,222,-42,8;193,223,-42,8;193,224,-42,8;193,225,-42,8" );
	mml_row( "193,226,-102,8;193,227,-66,8;193,228,-42,8;193,229,-42,8;194,224,-42,8;194,225,-42,8;194,226,-42,8;194,227,-42,8;194,228,-42,8;194,229,-42,8;194,244,-282,11;195,197,-246,1;195,198,-414,1;195,199,-378,1;195,200,-318,1;195,202,-282,1;195,224,-42,8;195,225,-42,8;195,226,-42,8;195,227,-42,8;195,228,-42,8;195,229,-42,8;195,242,-258,11;195,243,-282,11;195,244,-270,11" );
	mml_row( "196,196,-282,1;196,197,-258,1;196,198,-246,1;196,199,-390,1;196,200,-306,1;196,201,-282,1;196,202,-258,1;196,203,-234,1;196,226,-186,8;196,227,-42,8;196,228,-186,8;196,241,-268,11;196,242,-274,11;196,243,-282,11;196,244,-270,11;197,170,438,6;197,171,450,6;197,172,438,6;197,173,414,6;197,195,-330,1;197,196,-306,1;197,197,-282,1;197,198,-438,1;197,199,-438,1;197,200,-438,1" );
	mml_row( "197,201,-282,1;197,202,-246,1;197,204,247,1;197,226,-186,8;197,227,-186,8;197,228,-186,8;197,241,-277,11;197,242,-282,11;197,243,-282,11;197,244,-270,11;198,170,414,6;198,171,426,6;198,172,426,6;198,173,414,6;198,174,138,6;198,195,-162,1;198,196,-162,1;198,197,-330,1;198,198,-438,1;198,199,-438,1;198,200,-438,1;198,201,-438,1;198,203,222,1;198,204,366,1;198,242,-274,11" );
	mml_row( "198,243,-282,11;198,244,-282,11;199,170,426,6;199,171,426,6;199,172,426,6;199,173,426,6;199,174,138,6;199,175,138,6;199,195,-174,1;199,196,-174,1;199,197,-558,1;199,198,-618,1;199,199,-678,1;199,200,-678,1;199,201,-438,1;199,202,-678,1;199,203,-186,1;199,204,366,1;199,242,-274,11;199,243,-282,11;199,244,-282,11;200,169,426,6;200,170,426,6;200,172,126,6;200,173,114,6" );
	mml_row( "200,174,126,6;200,175,138,6;200,195,-174,1;200,196,-174,1;200,197,-558,1;200,198,-618,1;200,199,-678,1;200,200,-678,1;200,201,-426,1;200,202,-678,1;200,203,-186,1;200,204,-186,1;200,243,-282,11;200,244,-282,11;201,169,426,6;201,170,426,6;201,171,126,6;201,172,126,6;201,173,102,6;201,174,378,6;201,175,378,6;201,195,-162,1;201,196,-162,1;201,197,-534,1;201,198,-318,1" );
	mml_row( "201,199,-318,1;201,200,-318,1;201,201,-426,1;201,203,-186,1;201,204,-186,1;201,243,-282,11;201,244,-282,11;202,169,426,6;202,170,426,6;202,171,138,6;202,172,126,6;202,173,114,6;202,174,378,6;202,175,378,6;202,176,378,6;202,194,-78,1;202,195,-78,1;202,196,-162,1;202,197,-294,1;202,198,-306,1;202,199,-318,1;202,200,-318,1;202,201,-258,1;202,202,-246,1;202,203,-198,1" );
	mml_row( "202,204,-186,1;202,233,-222,13;202,234,-222,13;202,235,-222,13;203,170,390,6;203,171,390,6;203,173,402,6;203,174,126,6;203,175,354,6;203,176,333,6;203,196,-175,1;203,197,-294,1;203,198,-306,1;203,199,-366,1;203,200,-294,1;203,201,-270,1;203,202,-246,1;203,218,-54,14;203,233,-222,13;203,234,-222,13;203,235,-222,13;204,170,402,6;204,172,114,6;204,173,438,6;204,174,126,6" );
	mml_row( "204,176,258,6;204,199,-366,1;204,200,-306,1;204,201,-270,1;204,218,-54,14;204,219,-54,14;204,234,-222,13;204,235,-222,13;205,169,126,6;205,170,126,6;205,171,126,6;205,172,126,6;205,173,438,6;205,174,438,6;205,175,222,6;205,176,210,6;205,218,-54,14;205,219,-54,14;205,234,-234,13;205,235,-222,13;206,171,126,6;206,172,126,6;206,173,114,6;206,174,414,6;206,175,390,6" );
	mml_row( "206,176,138,6;206,177,126,6;206,218,-54,14;206,219,-54,14;207,171,126,6;207,172,378,6;207,173,402,6;207,174,390,6;207,175,378,6;207,176,126,6;207,177,126,6;207,218,-54,14;207,219,-54,14;208,171,378,6;208,172,378,6;208,173,126,6;208,174,378,6;208,175,378,6;208,176,126,6;208,177,150,6;208,178,162,6;209,171,378,6;209,172,378,6;209,173,378,6;209,174,378,6" );
	mml_row( "209,175,378,6;209,176,138,6;209,177,162,6;209,178,174,6;209,240,-258,12;209,241,-270,12;209,242,-270,12;209,243,-270,12;210,170,138,6;210,171,378,6;210,172,378,6;210,173,378,6;210,174,378,6;210,175,378,6;210,176,378,6;210,177,174,6;210,240,-258,12;210,241,-270,12;210,243,-270,12;211,170,138,6;211,171,126,6;211,174,378,6;211,175,378,6;211,176,378,6;211,238,-250,12" );
	mml_row( "211,239,-246,12;211,241,-270,12;211,242,-270,12;211,243,-270,12;212,174,390,6;212,175,378,6;212,176,378,4;212,176,378,6;212,181,-42,4;212,182,-54,4;212,183,-54,4;212,238,-246,12;212,239,-234,12;212,241,-270,12;212,242,-270,12;212,243,-270,12;213,175,378,4;213,176,378,4;213,177,54,4;213,178,42,4;213,179,18,4;213,180,-17,4;213,181,-42,4;213,182,-54,4;213,183,-30,4" );
	mml_row( "213,184,-30,4;213,238,-246,12;213,239,-246,12;213,241,-258,12;213,242,-258,12;214,174,127,4;214,175,114,4;214,176,66,4;214,177,30,4;214,178,30,4;214,179,18,4;214,180,-18,4;214,181,-42,4;214,182,-54,4;214,183,-30,4;214,184,-30,4;215,176,42,4;215,177,42,4;215,178,42,4;215,181,-42,4;215,182,-42,4;215,183,-30,4;216,232,-226,9;216,233,-208,9;216,234,-220,9" );
	mml_row( "216,240,-294,9;216,241,-282,9;216,242,-282,9;217,228,-198,15;217,232,-214,9;217,233,-226,9;217,234,-232,9;217,239,-294,9;217,240,-294,9;217,241,-282,9;217,242,-282,9;218,228,-210,15;218,229,-210,15;218,230,-210,15;218,233,-220,9;218,234,-226,9;218,235,-234,9;218,236,-234,9;218,237,-234,9;218,238,-258,9;218,239,-282,9;218,240,-282,9;218,241,-282,9;218,242,-282,9;219,228,-210,15" );
	mml_row( "219,229,-198,15;219,234,-220,9;219,235,-234,9;219,236,-234,9;219,237,-234,9;219,238,-258,9;219,239,-282,9;219,240,-282,9;219,241,-270,9;219,242,-270,9;219,245,-234,7;219,246,-234,7;219,247,-234,7;219,248,-234,7;219,249,-234,7;219,250,-234,7;220,228,-210,15;220,235,-234,9;220,236,-234,9;220,237,-246,9;220,238,-258,9;220,245,-234,7;220,246,-222,7;220,248,-222,7;220,249,-222,7" );
	mml_row( "220,250,-222,7;221,235,-234,9;221,236,-246,9;221,237,-246,9;221,238,-258,9;221,245,-234,7;221,246,-222,7;221,248,-222,7;221,249,-222,7;221,250,-234,7;222,207,50,3;222,208,50,3;222,235,-246,9;222,236,-222,9;222,245,-234,7;222,246,-222,7;222,248,-222,7;222,249,-222,7;222,250,-234,7;223,207,50,3;223,208,50,3;223,235,-222,9;223,236,-222,9;223,245,-234,7;223,246,-222,7" );
	mml_row( "223,247,-222,7;223,248,-222,7;223,249,-222,7;223,250,-234,7;224,207,50,3;224,208,50,3;224,242,-258,7;224,243,-258,7;224,244,-246,7;224,245,-234,7;224,246,-234,7;224,247,-234,7;224,248,-234,7;224,249,-234,7;224,250,-306,7;224,251,-306,7;224,252,-294,7;224,253,-294,7;224,254,-294,7;225,207,54,3;225,208,54,3;225,240,-306,5;225,241,-318,5;225,242,-258,7;225,243,-258,7" );
	mml_row( "225,244,-234,7;225,245,-234,7;225,246,-234,7;225,247,-234,7;225,248,-234,7;225,249,-270,7;225,250,-306,7;225,251,-306,7;225,252,-294,7;225,253,-294,7;225,254,-294,7;226,207,54,3;226,208,54,3;226,240,-360,5;226,241,-378,5;226,242,-258,5;226,242,-258,7;226,243,-258,5;226,243,-258,7;226,244,-246,7;226,245,-246,7;226,246,-246,7;226,247,-246,7;226,250,-306,7;226,251,-306,7" );
	mml_row( "226,252,-282,7;226,254,-294,7;227,207,-18,3;227,208,-18,3;227,240,-402,5;227,241,-426,5;227,242,-258,5;227,243,-258,5;227,250,-306,7;227,251,-306,7;227,252,-282,7;227,254,-294,7;227,255,-294,7;228,207,-78,3;228,208,-78,3;228,240,-450,5;228,241,-450,5;228,242,-258,5;228,243,-258,5;228,244,-486,5;228,250,-306,7;228,251,-306,7;228,252,-294,7;228,253,-294,7;228,254,-294,7" );
	mml_row( "229,207,-114,3;229,208,-126,3;229,209,-126,3;229,244,-510,5;229,245,-474,5;229,250,-306,7;229,251,-306,7;229,252,-294,7;229,253,-294,7;229,254,-294,7;230,207,-138,3;230,208,-150,3;230,209,-126,3;230,243,-522,5;230,244,-534,5;230,245,-474,5;230,246,-474,5;231,207,-138,3;231,208,-150,3;231,209,-126,3;231,211,-258,3;231,212,-270,3;231,213,-270,3;231,241,-510,5;231,242,-522,5" );
	mml_row( "231,243,-522,5;231,244,-522,5;231,245,-522,5;232,207,-150,3;232,208,-162,3;232,209,-162,3;232,210,-258,3;232,211,-270,3;232,212,-270,3;232,213,-258,3;232,241,-510,5;232,242,-510,5;232,243,-522,5;232,244,-522,5;232,245,-510,5;233,208,-186,3;233,209,-210,3;233,210,-246,3;233,211,-270,3;233,212,-282,3;233,213,-258,3;234,209,-222,3;234,210,-246,3;234,211,-258,3;234,212,-270,3" );
	mml_row( "234,213,-258,3;235,212,-258,3;164,194,-103,2;164,195,-103,2;165,194,-103,2;165,195,-103,2;164,196,-111,2;164,197,-111,2;165,196,-111,2;165,197,-111,2;166,192,-39,2;166,193,-39,2;167,192,-39,2;167,193,-39,2;166,194,-39,2;166,195,-39,2;167,194,-39,2;167,195,-39,2;166,196,-78,2;166,197,-78,2;167,196,-78,2;167,197,-78,2;166,198,7,2;166,199,7,2;167,198,7,2" );
	mml_row( "167,199,7,2;166,200,16,2;166,201,16,2;167,200,16,2;167,201,16,2;166,202,7,2;166,203,7,2;167,202,7,2;167,203,7,2;168,192,-39,2;168,193,-39,2;169,192,-39,2;169,193,-39,2;168,194,-39,2;168,195,-39,2;169,194,-39,2;169,195,-39,2;168,196,-30,2;168,197,-30,2;169,196,-30,2;169,197,-30,2;168,198,62,2;168,199,62,2;169,198,62,2;169,199,62,2" );
	mml_row( "168,200,62,2;168,201,62,2;169,200,62,2;169,201,62,2;168,202,16,2;168,203,16,2;169,202,16,2;169,203,16,2;170,194,-87,2;170,195,-87,2;171,194,-87,2;171,195,-87,2;170,196,-50,2;170,197,-50,2;171,196,-50,2;171,197,-50,2;170,198,116,2;170,199,116,2;171,198,116,2;171,199,116,2;170,200,129,2;170,201,129,2;171,200,129,2;170,202,130,2;170,203,130,2" );
	mml_row( "171,203,130,2" );
}

mml_inside( org )
{
	if ( org[ 0 ] > 9114 && org[ 0 ] < 11814 && org[ 1 ] > -9138 && org[ 1 ] < -6438 )
		return 1;
	return org[ 0 ] > -4872 && org[ 0 ] < 5128 && org[ 1 ] > -4192 && org[ 1 ] < 5808;
}

mml_diag()
{
	level endon( "end_game" );
	last = "";
	n = 0;
	for ( ;; )
	{
		cur = "diag=" + getdvar( "mm_diag" );
		n++;
		if ( n % 20 == 0 )
			logprint( "MMLUI ticks_per_packet_x10=" + getdvar( "mm_tpp" ) + "\n" );
		if ( cur != last )
		{
			logprint( "MMLUI " + cur + " state=" + getdvar( "mm_state" ) + "\n" );
			last = cur;
		}
		wait 1;
	}
}

mml_info()
{
	level endon( "end_game" );
	for ( ;; )
	{
		wait 0.1;
		players = get_players();
		if ( players.size == 0 || !isdefined( players[ 0 ] ) )
			continue;
		team = "axis";
		if ( isdefined( level.zombie_team ) )
			team = level.zombie_team;
		left = 0;
		foreach ( ai in getaiarray( team ) )
		{
			if ( isdefined( ai ) && isalive( ai ) && !isdefined( ai.is_giant_robot ) )
				left++;
		}
		// not spawned yet this round
		if ( isdefined( level.zombie_total ) && level.zombie_total > 0 )
			left += level.zombie_total;
		setdvar( "mm_info", left + " " + int( players[ 0 ].health ) + " " + int( players[ 0 ].maxhealth ) );
	}
}

mml_add_poi( list, org, type )
{
	return list + int( org[ 0 ] ) + "," + int( org[ 1 ] ) + "," + type + ";";
}

mml_perk_type( perk )
{
	if ( !isdefined( perk ) )
		return "";
	switch ( perk )
	{
		case "specialty_armorvest":
			return "J";
		case "specialty_quickrevive":
			return "R";
		case "specialty_fastreload":
			return "S";
		case "specialty_longersprint":
			return "M";
		case "specialty_additionalprimaryweapon":
			return "K";
		case "specialty_weapupgrade":
			return "P";
	}
	return "";
}

mml_feet()
{
	level endon( "end_game" );
	for ( ;; )
	{
		wait 0.05;
		list = "";
		if ( isdefined( level.a_giant_robots ) )
		{
			foreach ( robot in level.a_giant_robots )
			{
				if ( !isdefined( robot ) || !isdefined( robot.is_walking ) || !robot.is_walking )
					continue;
				list = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_LE" ), mml_foot( robot, "TAG_ATTACH_HATCH_LE" ) );
				list = mml_add_poi( list, robot gettagorigin( "TAG_ATTACH_HATCH_RI" ), mml_foot( robot, "TAG_ATTACH_HATCH_RI" ) );
			}
		}
		setdvar( "mm_feet", list );
	}
}

// 1 = this foot is coming down, 0 = otherwise
mml_foot( robot, tag )
{
	now = robot gettagorigin( tag );
	if ( !isdefined( robot.mml_z ) )
		robot.mml_z = [];
	last = robot.mml_z[ tag ];
	robot.mml_z[ tag ] = now[ 2 ];
	if ( isdefined( last ) && now[ 2 ] < last - 2 )
		return 1;
	return 0;
}

mml_gen_type( name, zone )
{
	// H = captured by the players, drawn as a green G
	g = "G";
	if ( isdefined( zone.ent_flag ) && isdefined( zone.ent_flag[ "player_controlled" ] ) && zone.ent_flag[ "player_controlled" ] )
		g = "H";
	if ( !isdefined( name ) )
		return g;
	switch ( name )
	{
		case "generator_start_bunker":
			return g + "1";
		case "generator_tank_trench":
			return g + "2";
		case "generator_mid_trench":
			return g + "3";
		case "generator_nml_right":
			return g + "4";
		case "generator_nml_left":
			return g + "5";
		case "generator_church":
			return g + "6";
	}
	return g;
}

mml_poi()
{
	level endon( "end_game" );
	for ( ;; )
	{
		list = "";
		foreach ( ent in getentarray( "zombie_vending", "targetname" ) )
		{
			type = mml_perk_type( ent.script_noteworthy );
			if ( type != "" )
				list = mml_add_poi( list, ent.origin, type );
		}
		if ( isdefined( level.chests ) && isdefined( level.chest_index ) && isdefined( level.chests[ level.chest_index ] ) && isdefined( level.chests[ level.chest_index ].origin ) )
			list = mml_add_poi( list, level.chests[ level.chest_index ].origin, "B" );
		setdvar( "mm_poi0", list );
		list = "";
		if ( isdefined( level.zone_capture ) && isdefined( level.zone_capture.zones ) )
		{
			foreach ( zone in level.zone_capture.zones )
			{
				if ( isdefined( zone.origin ) )
					list = mml_add_poi( list, zone.origin, mml_gen_type( zone.script_noteworthy, zone ) );
			}
		}
		foreach ( ent in getentarray( "random_perk_machine", "targetname" ) )
			list = mml_add_poi( list, ent.origin, "W" );
		setdvar( "mm_poi1", list );
		wait 2;
	}
}

// name of the place the host is in, from the zone volumes of the map
mml_zone()
{
	level endon( "end_game" );
	mml_zone_names();
	wait 1;
	vols = getentarray( "player_volume", "script_noteworthy" );
	last = undefined;
	for ( ;; )
	{
		wait 0.3;
		players = get_players();
		if ( players.size == 0 || !isdefined( players[ 0 ] ) )
			continue;
		me = players[ 0 ];
		special = mml_part_name( mml_under( me.origin ) );
		if ( special != "" )
		{
			last = undefined;
			setdvar( "mm_zone", special );
			continue;
		}
		if ( isdefined( last ) && me istouching( last ) )
			continue;
		last = undefined;
		for ( i = 0; i < vols.size; i++ )
		{
			vol = vols[ i ];
			if ( !isdefined( vol ) || !isdefined( vol.targetname ) || !isdefined( level.mml_names[ vol.targetname ] ) )
				continue;
			if ( me istouching( vol ) )
			{
				last = vol;
				setdvar( "mm_zone", level.mml_names[ vol.targetname ] );
				break;
			}
		}
	}
}

mml_zone_names()
{
	level.mml_names = [];
	level.mml_names[ "ug_bottom_zone" ] = "CRIPTA";
	level.mml_names[ "zone_air_stairs" ] = "CUEVA DE VIENTO";
	level.mml_names[ "zone_air_stairs_1" ] = "CUEVA DE VIENTO";
	level.mml_names[ "zone_bolt_stairs" ] = "CUEVA DE RAYO";
	level.mml_names[ "zone_bolt_stairs_1" ] = "CUEVA DE RAYO";
	level.mml_names[ "zone_bunker_1" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_1a" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_2" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_2a" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_3a" ] = "TRINCHERA CENTRAL - G3";
	level.mml_names[ "zone_bunker_3b" ] = "TRINCHERA CENTRAL - G3";
	level.mml_names[ "zone_bunker_4a" ] = "BUNKER DEL TANQUE - G2";
	level.mml_names[ "zone_bunker_4b" ] = "BUNKER DEL TANQUE - G2";
	level.mml_names[ "zone_bunker_4c" ] = "BUNKER DEL TANQUE - G2";
	level.mml_names[ "zone_bunker_4d" ] = "BUNKER DEL TANQUE - G2";
	level.mml_names[ "zone_bunker_4e" ] = "ESTACION DEL TANQUE";
	level.mml_names[ "zone_bunker_4f" ] = "BUNKER DEL TANQUE - G2";
	level.mml_names[ "zone_bunker_5a" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_5b" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_6" ] = "TRINCHERAS";
	level.mml_names[ "zone_bunker_tank_a" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_a1" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_a2" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_b" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_c" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_c1" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_d" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_d1" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_e" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_e1" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_e2" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_bunker_tank_f" ] = "CAMINO DEL TANQUE";
	level.mml_names[ "zone_chamber_0" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_1" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_2" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_3" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_4" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_5" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_6" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_7" ] = "CRAZY PLACE";
	level.mml_names[ "zone_chamber_8" ] = "CRAZY PLACE";
	level.mml_names[ "zone_fire_stairs" ] = "CUEVA DE FUEGO";
	level.mml_names[ "zone_fire_stairs_1" ] = "CUEVA DE FUEGO";
	level.mml_names[ "zone_ice_stairs" ] = "CUEVA DE HIELO";
	level.mml_names[ "zone_ice_stairs_1" ] = "CUEVA DE HIELO";
	level.mml_names[ "zone_nml_0" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_1" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_10" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_10a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_11" ] = "ZONA DE JUGGERNOG - G4";
	level.mml_names[ "zone_nml_11a" ] = "ZONA DE JUGGERNOG - G4";
	level.mml_names[ "zone_nml_12" ] = "ZONA DE JUGGERNOG - G4";
	level.mml_names[ "zone_nml_12a" ] = "ZONA DE JUGGERNOG - G4";
	level.mml_names[ "zone_nml_13" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_14" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_15" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_15a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_16" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_16a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_17" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_17a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_18" ] = "MID - EXCAVACION";
	level.mml_names[ "zone_nml_19" ] = "MID - EXCAVACION";
	level.mml_names[ "zone_nml_2" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_20" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_2a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_2b" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_3" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_4" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_5" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_6" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_7" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_7a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_8" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_9" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_9a" ] = "TIERRA DE NADIE";
	level.mml_names[ "zone_nml_celllar" ] = "SOTANO DE LA GRANJA";
	level.mml_names[ "zone_nml_farm" ] = "GRANJA - G5";
	level.mml_names[ "zone_nml_farm_1" ] = "GRANJA - G5";
	level.mml_names[ "zone_start" ] = "LABORATORIO";
	level.mml_names[ "zone_start_a" ] = "LABORATORIO";
	level.mml_names[ "zone_start_b" ] = "LABORATORIO";
	level.mml_names[ "zone_village_0" ] = "ALDEA";
	level.mml_names[ "zone_village_1" ] = "IGLESIA - ABAJO";
	level.mml_names[ "zone_village_1a" ] = "ESTACION DEL TANQUE";
	level.mml_names[ "zone_village_2" ] = "IGLESIA";
	level.mml_names[ "zone_village_3" ] = "DETRAS DE LA IGLESIA - G6";
	level.mml_names[ "zone_village_3a" ] = "DETRAS DE LA IGLESIA - G6";
	level.mml_names[ "zone_village_3b" ] = "DETRAS DE LA IGLESIA - G6";
	level.mml_names[ "zone_village_4" ] = "ALDEA";
	level.mml_names[ "zone_village_4a" ] = "ALDEA";
	level.mml_names[ "zone_village_4b" ] = "ALDEA";
	level.mml_names[ "zone_village_5" ] = "ALDEA";
	level.mml_names[ "zone_village_5a" ] = "ALDEA";
	level.mml_names[ "zone_village_5b" ] = "ALDEA";
	level.mml_names[ "zone_village_6" ] = "ALDEA";
	level.mml_names[ "zone_village_6a" ] = "ALDEA";
}

mml_part_name( part )
{
	switch ( part )
	{
		case 1:
			return "CRIPTA";
		case 2:
			return "CUEVA DE RAYO";
		case 3:
			return "CUEVA DE VIENTO";
		case 4:
			return "CUEVA DE HIELO";
		case 5:
			return "CUEVA DE FUEGO";
	}
	return "";
}
