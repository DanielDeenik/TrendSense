#!/bin/bash

# Create necessary directories
mkdir -p uploads
mkdir -p migrations

# Install required packages
npm install express cors dotenv drizzle-orm drizzle-zod postgres multer uuid zod
npm install -D typescript ts-node @types/express @types/cors @types/multer @types/uuid drizzle-kit

# Create tsconfig.json
cat > tsconfig.json << EOL
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules"]
}
EOL

# Create drizzle.config.ts for database migrations
cat > drizzle.config.ts << EOL
import type { Config } from "drizzle-kit";
import { config } from "dotenv";

config();

export default {
  schema: "./shared/schema.ts",
  out: "./migrations",
  driver: "pg",
  dbCredentials: {
    connectionString: process.env.DATABASE_URL || "postgresql://postgres:postgres@localhost:5432/trendsense"
  }
} satisfies Config;
EOL

# Create a db-push script for database migrations
mkdir -p scripts
cat > scripts/db-push.ts << EOL
import { drizzle } from "drizzle-orm/postgres-js";
import { migrate } from "drizzle-orm/postgres-js/migrator";
import postgres from "postgres";
import * as schema from "../shared/schema";
import * as dotenv from "dotenv";

dotenv.config();

async function main() {
  const connectionString = process.env.DATABASE_URL;

  if (!connectionString) {
    console.error("DATABASE_URL environment variable is not set");
    process.exit(1);
  }

  // Connect to the database
  const client = postgres(connectionString);
  const db = drizzle(client, { schema });

  // Run migrations
  console.log("Running migrations...");
  await migrate(db, { migrationsFolder: "./migrations" });
  console.log("Migrations complete!");

  // Close the database connection
  await client.end();
}

main().catch((error) => {
  console.error("Migration error:", error);
  process.exit(1);
});
EOL

# Create .env file for local development
cat > .env << EOL
DATABASE_URL=${DATABASE_URL}
PORT=3000
NODE_ENV=development
EOL

# Create a start script
cat > start.sh << EOL
#!/bin/bash
npm install
npx ts-node server/index.ts
EOL

chmod +x start.sh

echo "Project setup complete!"
echo "-----------------------"
echo "Run the application with: ./start.sh"
echo "Generate database migrations with: npx drizzle-kit generate:pg"
echo "Push schema changes to the database with: npx ts-node scripts/db-push.ts"