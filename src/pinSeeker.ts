import { PythonShell } from 'python-shell';

type Coordinates = {
    count: number;
    points: {
        x: number;
        y: number;
    }[]
};

const log = (message: any) => {
    console.log(`[PinSeeker] ${message}`);
}

export class PinSeeker {
    static scriptPath = `${__dirname}/pinSeeker.py`;
    
    static async find(imageData: ArrayBufferLike): Promise<Coordinates> {
        log('Looking for pins...');
        const result = await new Promise((resolve, reject) => {
            const pyShell = new PythonShell(this.scriptPath,{mode:'binary'});

            let output = ""

            pyShell.stdout.on('data', x => {output += x.toString()});
            pyShell.stdout.on('end', () => {
                resolve(JSON.parse(output));
            });


            pyShell.on('error', e => reject(e));

            pyShell.send(imageData);
            
            pyShell.end(() => {});
        });

        return result as Coordinates;
    }
}
