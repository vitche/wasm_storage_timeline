package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"syscall/js"
)

// readInt64 reads an int64 from a buffer
func readInt64(buf *bytes.Buffer) (int64, error) {
	var value int64
	err := binary.Read(buf, binary.BigEndian, &value)
	return value, err
}

// readBufferWasm reads multiple Length-Timestamp-Buffer records from a binary buffer
func readBufferWasm(this js.Value, args []js.Value) interface{} {
	// Get binary data from JS Uint8Array
	data := make([]byte, args[0].Length())
	js.CopyBytesToGo(data, args[0])
	buf := bytes.NewBuffer(data)

	// Store parsed records
	var records []interface{}

	// Loop to read multiple records
	for buf.Len() > 0 {
		payloadSize, err := readInt64(buf)
		if err != nil {
			fmt.Println("Failed to read payload size:", err)
			break
		}

		// Read timestamp
		timestamp, err := readInt64(buf)
		if err != nil {
			fmt.Println("Failed to read timestamp:", err)
			break
		}

		// Read value (remaining bytes of this record)
		valueSize := int(payloadSize - 8) // Exclude timestamp size
		value := buf.Next(valueSize) // Efficiently extract bytes

		// Create JS object representation
		record := map[string]interface{}{
			"timestamp": timestamp,
			"value":     string(value),
		}

		records = append(records, record)
	}

	return records
}

// Expose functions to JavaScript
func main() {
	js.Global().Set("readBufferWasm", js.FuncOf(readBufferWasm))
	<-make(chan struct{}) // Blocks but allows JS interaction
}
