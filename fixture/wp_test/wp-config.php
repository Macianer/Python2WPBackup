<?php

define('DB_NAME', 'dbname');    // The name of the database
define('DB_USER', 'user');     // Your MySQL username
define('DB_PASSWORD', 'password'); // ...and password
define('DB_HOST', 'mysql.domain.xyz.de');    // 99% chance you won't need to change this value

$table_prefix  = 'wp_';   // Only numbers, letters, and underscores please!
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');
define('AUTH_KEY', 'anyString'); // Trage hier eine beliebige, m�glichst zuf�llige Phrase ein.
define('SECURE_AUTH_KEY', 'anyString'); // Trage hier eine beliebige, m�glichst zuf�llige Phrase ein.
define('LOGGED_IN_KEY', 'anyString'); // Trage hier eine beliebige, m�glichst zuf�llige Phrase ein.
define('NONCE_KEY', 'anyString'); // Trage hier eine beliebige, m�glichst zuf�llige Phrase ein.
define('AUTH_SALT',        'anyString');
define('SECURE_AUTH_SALT', 'anyString');
define('LOGGED_IN_SALT',   'anyString');
define('NONCE_SALT',       'anyString');
define ('WPLANG', 'de_DE');
define('WP_DEBUG', false);
/* That's all, stop editing! Happy blogging. */

if ( !defined('ABSPATH') )
   define('ABSPATH', dirname(__FILE__) . '/');
require_once(ABSPATH.'wp-settings.php');
?>
